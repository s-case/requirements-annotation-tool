import os
import re
import shutil
from readann import Project
from OntParser import ExtOntology
from transformationmap import transformit, transformitreverse

def add_project_to_ontology(projc, filename, req_to_read = None):
	tontology = ExtOntology(filename)
	if (not req_to_read):
		tontology.add_individual("Project", projc.name)
	for i, requirement in enumerate(projc.requirements()):
		if (not req_to_read) or req_to_read == i + 1:
			tontology.add_individual("Requirement", requirement[0], requirement[1])
			if (not req_to_read):
				tontology.add_property(projc.name, "project_has_requirement", requirement[0])
				tontology.add_property(requirement[0], "is_of_project", projc.name)
	for reqid, entity, addit in projc.entities():
		if addit:
			tontology.add_individual(transformit[entity[0]], entity[1], entity[2])
		if tontology.is_operation(transformit[entity[0]]):
			tontology.add_property(reqid, "requirement_has_operation", entity[1])
			tontology.add_property(entity[1], "is_operation_of_requirement", reqid)
		else:
			tontology.add_property(reqid, "requirement_has_concept", entity[1])
			tontology.add_property(entity[1], "is_concept_of_requirement", reqid)
		#print transformit[entity[0]], entity[1], entity[2]
	for association in projc.associations():
		tontology.add_property(association[0], transformit[association[1]], association[2])
		tontology.add_property(association[2], transformitreverse[association[1]], association[0])
		#print association[0], transformit[association[1]], association[2]
		#print association[2], transformitreverse[association[1]], association[0]
	tontology.close()

class ReadProject:
	def __init__(self):
		self.allpaths = []

	def read_project(self, project_path, project_name, pform):
		if pform.endswith('s'):
			non_blank_count = 0
			with open(project_path + '/' + project_name + '.txt') as infp:
				for line in infp:
					if line.strip():
						non_blank_count += 1
			owlfiles, ttlfiles = [], []
			for i in range(1, non_blank_count + 1):
				shutil.copy2('/brat/original_ontology/requirements.owl', project_path + '/' + project_name + str(i) + '.owl')
				p = Project(project_name, project_path + '/' + project_name, i)
				add_project_to_ontology(p, project_path + '/' + project_name + str(i) + '.owl', i)
				owlfiles.append(project_path + '/' + project_name + str(i) + '.owl')
				ttlfiles.append(project_path + '/' + project_name + str(i) + '.ttl')
				self.allpaths.append(project_path + '/' + project_name + str(i) + '.owl')
				self.allpaths.append(project_path + '/' + project_name + str(i) + '.ttl')
			return owlfiles, ttlfiles
		else:
			shutil.copy2('/brat/original_ontology/requirements.owl', project_path + '/' + project_name + '.owl')
			p = Project(project_name, project_path + '/' + project_name)
			add_project_to_ontology(p, project_path + '/' + project_name + '.owl')
			self.allpaths.append(project_path + '/' + project_name + '.owl')
			self.allpaths.append(project_path + '/' + project_name + '.ttl')
			return project_path + '/' + project_name + '.owl', project_path + '/' + project_name + '.ttl'

	def clean_up(self):
		for anpath in self.allpaths:
			os.remove(anpath)

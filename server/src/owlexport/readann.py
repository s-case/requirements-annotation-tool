
class Entity:
	def __init__(self, entity_id, entity_type, entity_text):
		self.entity_id = entity_id
		self.entity_type = entity_type
		self.entity_text = '_'.join(entity_text.split())
	def __str__(self):
		return str(self.entity_id) + "." + self.entity_text + ":" + self.entity_type
	def owl(self):
		return self.entity_type, self.entity_text + "_" + str(self.entity_id), self.entity_text
	def nameid(self):
		return self.entity_text + "_" + str(self.entity_id)

class Association:
	def __init__(self, association_id, association_type, entity_a, entity_b):
		self.association_id = association_id
		self.association_type = association_type
		self.entity_a = entity_a
		self.entity_b = entity_b
	def __str__(self):
		return str(self.association_id) + "." + self.association_type + ":" + str(self.entity_a) + "-" + str(self.entity_b)
	def owl(self):
		return self.entity_a, self.association_type, self.entity_b

class Requirement:
	def __init__(self, requirement_text, requirement_id):
		self.reqid = requirement_id
		self.reqtext = requirement_text.replace(':', '_').replace('/', '_').replace('\'', '_').replace('\xe2\x80\x99', '_')
		self.entities = []
		self.associations = []
	def add_entity(self, entity_data):
		self.entities.append(Entity(int(entity_data[0][1:]), entity_data[1].split()[0], entity_data[-1]))
		#print self.entities[-1]
	def has_entity(self, entity_id):
		return entity_id in [s.entity_id for s in self.entities]
	def add_association(self, association_data):
		assoc = association_data[-1].split()
		self.associations.append(Association(int(association_data[0][1:]), assoc[0], int(assoc[1].split(':T')[-1]), int(assoc[2].split(':T')[-1])))
		#print self.associations[-1]
	def __str__(self):
		txtt = "Requirement " + str(self.reqid) + "\n"
		txtt = "Text: " + self.reqtext + "\n"
		txtt += "Entities: (" + '), ('.join(map(str, self.entities)) + ")\n"
		txtt += "Associations: (" + '), ('.join(map(str, self.associations)) + ")\n"
		return txtt
	def get_entity_by_id(self, entity_id):
		return [s for s in self.entities if s.entity_id == entity_id][0]
	def get_entities(self):
		for entity in self.entities:
			yield entity.owl()
	def get_associations(self):
		for association in self.associations:
			a, r, b = association.owl()
			a = self.get_entity_by_id(a)
			b = self.get_entity_by_id(b)
			yield a.owl(), r, b.owl()
	def treqid(self):
		return 'FR' + str(self.reqid)

class Project:
	def __init__(self, name, filename, req_to_read = None):
		self.req_to_read = req_to_read
		self.name = name
		self.reqs = []
		self.read_ann(filename)

	def read_ann(self, filename):
		with open(filename + '.txt') as txtfile:
			passage = txtfile.read()
			sentences = [s.strip() for s in passage.split('\n') if s.strip()]
			for i, sentence in enumerate(sentences):
				self.reqs.append(Requirement(sentence, i + 1))
		def get_reqid_by_index(indexb):
			return passage[0:indexb].count('\n')
		def get_reqid_by_entity_index(indexb):
			for i, req in enumerate(self.reqs):
				if req.has_entity(indexb):
					return i
			return None
		with open(filename + '.ann') as annfile:
			annotations = [s.strip() for s in annfile.readlines()]
		
		for annotation in annotations:
			if annotation[0] == 'T':
				#entity
				annotation = annotation.split('\t')
				reqid = get_reqid_by_index(int(annotation[1].split()[-1]))
				if (not self.req_to_read) or reqid == self.req_to_read - 1:
					self.reqs[reqid].add_entity(annotation)
			elif annotation[0] == 'R':
				#association
				annotation = annotation.split('\t')
				reqid = get_reqid_by_entity_index(int(annotation[-1].split()[-1].split(':T')[-1]))
				if (not self.req_to_read) or reqid == self.req_to_read - 1:
					self.reqs[reqid].add_association(annotation)
		#for req in reqs:
		#	print req

	def requirements(self):
		return ((req.treqid(), req.reqtext) for req in self.reqs)

	def entities(self):
		self.namecorr = {}
		self.entitycorr = {}
		for req in self.reqs:
			for entity in req.get_entities():
				if entity[0] + entity[2] not in self.entitycorr:
					if entity[2] not in self.namecorr:
						self.namecorr[entity[2]] = 0
					else:
						self.namecorr[entity[2]] += 1
					self.entitycorr[entity[0] + entity[2]] = (entity[2] + '_' + str(self.namecorr[entity[2]])) if self.namecorr[entity[2]] > 0 else entity[2]
					yield req.treqid(), (entity[0], self.entitycorr[entity[0] + entity[2]], entity[2]), True
				else:
					yield req.treqid(), (entity[0], self.entitycorr[entity[0] + entity[2]], entity[2]), False

	def associations(self):
		for _ in self.entities():
			pass
		assocset = set()
		for req in self.reqs:
			for association in req.get_associations():
				entity0 = association[0]
				entity1 = association[2]
				if self.entitycorr[entity0[0] + entity0[2]] + association[1] + self.entitycorr[entity1[0] + entity1[2]] not in assocset:
					assocset.add(self.entitycorr[entity0[0] + entity0[2]] + association[1] + self.entitycorr[entity1[0] + entity1[2]])
					yield self.entitycorr[entity0[0] + entity0[2]], association[1], self.entitycorr[entity1[0] + entity1[2]]
#p = Project('Restmarks')
#for req in p.reqs:
#	print req
#p.entities()
#p.associations()
#for requirement in p.requirements():
#	print requirement


import re
import os.path

class HieroFont(object):
	"""Class for a Hiero-generated bitmap font"""

	# quote-aware splitting and unquoting using RE_SPLIT.findall
	RE_SPLIT = re.compile(r"\S+='.*?'|\S+=\".*?\"|\S+")
	RE_UNQUOTE = re.compile(r"'(.*?)'|\"(.*?)\"|(\S+)")

	def __init__(self, font_file):

		self.info = {}
		self.common = {}

		self.pages = {}
		self.chars = {}

		self.filename = font_file
		self.basedir = os.path.dirname(font_file)

		f = open(font_file)
		
		for line in f:

			

			# quote-aware split of line, then unquote all matches
			l = [ "".join(m) for m in HieroFont.RE_SPLIT.findall(line) ]

			command = l[0]
			l = l[1:]
			
			vals = { k: ["".join(m) for m in HieroFont.RE_UNQUOTE.findall(v)][0]  for k,v in ( elem.split("=") for elem in l ) }

			if command == "info":
				self.info = vals

			elif command == "common":
				self.common = vals

			elif command == "page":
				self.pages[vals['id']] = self._get_page(vals['id'], vals['file'])

			elif command == "chars":
				pass

			elif command == "char":
				for k in ["id", "x", "y", "width", "height", "xadvance", "xoffset", "yoffset"]:
					vals[k] = int(vals[k])

				self.chars[chr(vals['id'])] = vals
			
			else:
				raise Exception("Unknown command: {0}".format(command))

		pass

	def _get_page(self, id, file, basedir):
		return file

	def get_alphabet(self):
		return sorted(self.chars.keys())

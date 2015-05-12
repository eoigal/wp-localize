from HTMLParser import HTMLParser
import sublime, sublime_plugin, logging


class WpLocalizeCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		p = MyParser()
		for region in self.view.sel():
			if not region.empty():
				replacement = self.view.substr(region).replace( "'", "\\'" )
				p.feed(replacement)
				urls = p.output_list 
				if not urls:
					#just reg string
					replacement = "<?php _e( '%s' ); ?>" % replacement
				else:
					#has urls - need to strip them out and replace with placeholders
					i = 1
					url_args = "'%s'" % "', '".join( urls )
					for url in urls:
						replacement = replacement.replace( url, '%%%ds' % i )
						i += 1
					replacement = "<?php printf( __( '%s' ), %s ); ?>" % ( replacement, url_args )

				args['contents'] = replacement
	       		self.view.run_command('insert_snippet', args)




class MyParser(HTMLParser):
	def __init__(self, output_list=None):
		HTMLParser.__init__(self)
		if output_list is None:
			self.output_list = []
		else:
			self.output_list = output_list

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			self.output_list.append(dict(attrs).get('href'))

	
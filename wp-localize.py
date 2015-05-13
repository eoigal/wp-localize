from HTMLParser import HTMLParser
import sublime, sublime_plugin, re, logging

class WpLocalizeBase(sublime_plugin.TextCommand):

	def is_escaped(self):
  		return self.escape_type() != 'none'

	def run(self, edit, **args):	
		for region in self.view.sel():
			if not region.empty():
				selected_text = self.view.substr(region)

				#check if a string assignment i.e. $something = 'some string' or array( 'key' => 'some value' )
				if ( selected_text[0] == "'" and selected_text[-1] == "'" ) or ( selected_text[0] == '"' and selected_text[-1] == '"' ):
					selected_text = selected_text[1:-1]
					replacement   = self.get_replacement_string( selected_text )
					#need to replace _e( with __( and printf with sprintf
					replacement = replacement.replace( '_e(', '__(' ).replace( 'printf', 'sprintf' )
				else:
					replacement = "<?php %s; ?>" % self.get_replacement_string( selected_text )

				#if escaped, need to replace translation methods with escaped translation methods
				if self.is_escaped():
					if self.escape_type() == 'html':
						replacement = replacement.replace( '__(', 'esc_html__(' )
						replacement = replacement.replace( '_e(', 'esc_html_e(' )
					elif self.escape_type() == 'attr':
						replacement = replacement.replace( '__(', 'esc_attr__(' )
						replacement = replacement.replace( '_e(', 'esc_attr_e(' )

				args['contents'] = replacement
	       		self.view.run_command('insert_snippet', args)

	def get_replacement_string( self, selected_text ):
		p = MyParser()
		p.feed(selected_text)
		#make sure all attrs in selected text use double quotes - easier to parse
		for key,value in p.output_attrs:
			rgx = r"%s\w?=\w?'%s'" % ( key, value )
			replace = r'%s="%s"' % ( key, value )
			selected_text = re.sub( rgx, replace, selected_text );

		urls = p.output_list 
		if not urls:
			#just reg string
			replacement = "_e( '%s' )" % selected_text.replace( "'", "\\'" )
		else:
			#has urls - need to strip them out and replace with placeholders
			i = 1
			url_args = "'%s'" % "', '".join( urls )
			for url in urls:
				find = 'href="%s"' % url
				replace = 'href="%s"' % ( '%%%d\$s' % i  )
				logging.warning( replace )
				selected_text = selected_text.replace( find, replace )
				i += 1
			replacement = "printf( __( '%s' ), %s )" % ( selected_text.replace( "'", "\\'" ), url_args )

		return replacement



class WpLocalizeCommand(WpLocalizeBase):
	def escape_type(self):
		return 'none'

class WpLocalizeAndEscapeHtmlCommand(WpLocalizeBase):
	def escape_type(self):
		return 'html'

class WpLocalizeAndEscapeAttrCommand(WpLocalizeBase):
	def escape_type(self):
		return 'attr'

class MyParser(HTMLParser):
	def __init__(self, output_list=None, output_attrs=None):
		HTMLParser.__init__(self)

		if output_list is None:
			self.output_list = []
		else:
			self.output_list = output_list

		if output_attrs is None:
			self.output_attrs = []
		else:
			self.output_attrs = output_attrs

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			self.output_list.append(dict(attrs).get('href'))
		for attr in attrs:
			self.output_attrs.append(attr)

	
from HTMLParser import HTMLParser
import sublime, sublime_plugin, re, collections, logging

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

	def is_number(self, s):
	    try:
	        float( s )
	        return True
	    except ValueError:
	        return False

	def get_replacement_string( self, selected_text ):
		p = MyParser()
		p.feed(selected_text)
		#make sure all attrs in selected text use double quotes - easier to parse
		for key,value in p.output_attrs:
			rgx = r"%s\w?=\w?'%s'" % ( key, value )
			replace = r'%s="%s"' % ( key, value )
			selected_text = re.sub( rgx, replace, selected_text );

		settings    = sublime.load_settings('wp-localize.sublime-settings');
		text_domain = settings.get('text_domain');
		ending      = ')'
		if ( text_domain ):
			ending = ", '%s' )" % text_domain

		#find any numbers in text
		rgx = re.compile("(\d[\d,. ]+)")
		numbers = rgx.findall(selected_text)
		numbers = set( numbers )
		urls    = set( p.output_list )
		
		if not urls and not numbers:
			#just reg string
			replacement = "_e( '%s' %s" % ( selected_text.replace( "'", "\\'" ).replace( "$", "\$" ), ending )
		elif urls and not numbers:
			#has urls - need to strip them out and replace with placeholders
			urls = set( urls )
			i = 1
			url_args = "'%s'" % "', '".join( urls )
			for url in urls:
				find = 'href="%s"' % url
				replace = 'href="%s"' % ( '%%%d\$s' % i  )
				selected_text = selected_text.replace( find, replace )
				i += 1
			replacement = "printf( __( '%s' %s, %s )" % ( selected_text.replace( "'", "\\'" ).replace( "$", "\$" ), ending, url_args )
		else:
			#has urls and numbers- need to strip them out and replace with placeholders
			positions = {}

			#need to find position of urls and numbers, then need to sort args for the printf
			for number in numbers:
				if self.is_number( number.replace( ',', '' ) ):
					if number.find( ',' ) != -1: 
						t = 'string'
					elif number.find( '.' ) != -1: 
						t = 'float'
					else:
						t = 'number'

					pos = selected_text.index( number )
					positions[ pos ] = { 'type': t, 'value': number, 'find': number, 'replace': '' }

			for url in urls:
				find    = u'href="%s"' % url
				replace = u'href="%%%d$s"'
				positions[selected_text.index( find ) ] = { 'type': 'url', 'value': url, 'find': find, 'replace' : replace }

			i = 0
			url_args = ''

			for key in sorted( positions ):
				find = positions[key].get( 'find' )

				i += 1

				if ( positions[key].get( 'type' ) == 'url' ):
					replace = positions[key].get( 'replace' ) % i
					url_args += "'%s', " % str( positions[key].get( 'value' ) )
				elif ( positions[key].get( 'type' ) == 'float' ):
					replace = '%%%d$f ' % i
					url_args += positions[key].get( 'value' ) + ", "
				elif ( positions[key].get( 'type' ) == 'string' ):
					replace = '%%%d$s ' % i
					url_args += "number_format_i18n('%s'), " % str( positions[key].get( 'value' ).replace( ',', '' ).replace( ' ', '' ) )
				elif ( positions[key].get( 'type' ) == 'number' ):
					replace = '%%%d$d ' % i
					url_args += "%d, " % int( positions[key].get( 'value' ) )

				selected_text = selected_text.replace( find, replace )

			replacement = "printf( __( '%s' %s, %s )" % ( selected_text.replace( "'", "\\'" ).replace( "$", "\$" ), ending, url_args[:-2] )

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

	
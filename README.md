# wp-localize
Sublime Text plugin that localizes a selected string using the WordPress i18n translation methods.

This plugin will parse a string of selected text and work out what i18n method to encase the string in.

The plugin has one main assumption; if the selected text is encased in single or double quotes, its assumed the string is used in php code and as such we don't want to echo or print the string

Also, this plugin does not handle every i18n method, just the following most common methods;

* __()
* _e()
* esc_html__()
* esc_html_e()
* esc_attr__()
* esc_attr_e()

Not supported

* _n() Plurals
* _x() Context

<h1>Typical Uses</h1>

<b>Normal text</b>
```
Follow the yellow brick road
```

```
<!-- ctrl + shift + d to localize string -->
<?php _e( 'Follow the yellow brick road' , 'some-text-domain' ); ?>
<!-- ctrl + shift + e to html escape -->
<?php esc_html_e( 'Follow the yellow brick road' , 'some-text-domain' ); ?>
<!-- ctrl + shift + a to attribute escape -->
<?php esc_html_attr( 'Follow the yellow brick road' , 'some-text-domain' ); ?>
```

<b>Normal text surrounded with QUOTES</b>
```
'Follow the yellow brick road'
```

```
<!-- ctrl + shift + d to localize string -->
__( 'Follow the yellow brick road' , 'some-text-domain' )
<!-- ctrl + shift + e to html escape -->
esc_html__( 'Follow the yellow brick road' , 'some-text-domain' )
<!-- ctrl + shift + d to attribute escape -->
esc_attr__( 'Follow the yellow brick road' , 'some-text-domain' )
```

<b>Text with URLs and Numbers</b>
```
I'd like 19,876.23 <a href="http://dictionary.com">words</a> in 100 to <a href="#type=sentence">5,000 sentences</a>
```

```
<!-- ctrl + shift + d to localize string -->
<?php printf( __( 'I\'d like %1$s <a href="%2$s">words</a> in %3$d to <a href="%4$s">%5$s sentences</a>' , 'some-text-domain' ), number_format_i18n('19876.23'), 'http://dictionary.com', 100, '#type=sentence', number_format_i18n('5000') ); ?>
<!-- ctrl + shift + e to html escape -->
<?php printf( esc_html__( 'I\'d like %1$s <a href="%2$s">words</a> in %3$d to <a href="%4$s">%5$s sentences</a>' , 'some-text-domain' ), number_format_i18n('19876.23'), 'http://dictionary.com', 100, '#type=sentence', number_format_i18n('5000') ); ?>
<!-- ctrl + shift + a to attribute escape -->
<?php printf( esc_attr__( 'I\'d like %1$s <a href="%2$s">words</a> in %3$d to <a href="%4$s">%5$s sentences</a>' , 'some-text-domain' ), number_format_i18n('19876.23'), 'http://dictionary.com', 100, '#type=sentence', number_format_i18n('5000') ); ?>
```

<b>Text with URLs and Numbers surrounded with QUOTES</b>
```
'I'd like 19,876.23 <a href="http://dictionary.com">words</a> in 100 to <a href="#type=sentence">5,000 sentences</a>'
```

```
<!-- ctrl + shift + d to localize string -->
sprintf( __( 'I\'d like %1$s <a href="%2$s">words</a> in %3$d to <a href="%4$s">%5$s sentences</a>' , 'some-text-domain' ), number_format_i18n('19876.23'), 'http://dictionary.com', 100, '#type=sentence', number_format_i18n('5000') )
<!-- ctrl + shift + e to html escape -->
sprintf( esc_html__( 'I\'d like %1$s <a href="%2$s">words</a> in %3$d to <a href="%4$s">%5$s sentences</a>' , 'some-text-domain' ), number_format_i18n('19876.23'), 'http://dictionary.com', 100, '#type=sentence', number_format_i18n('5000') )
<!-- ctrl + shift + d to attribute escape -->
sprintf( esc_attr__( 'I\'d like %1$s <a href="%2$s">words</a> in %3$d to <a href="%4$s">%5$s sentences</a>' , 'some-text-domain' ), number_format_i18n('19876.23'), 'http://dictionary.com', 100, '#type=sentence', number_format_i18n('5000') )
```

<h3>Setup</h3>
* Copy the plugin folder to your Sublime Text Packages folder
* Copy the key bindings to the Sublime Text Default Key Bindings - User
* Update the text domain to whatever slug your theme/plugin uses - leave blank to not include text domain argument in i18n methods
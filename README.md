# wp-localize
Sublime Text plugin that localizes a selected string using the WordPress i18n translation methods.

This plugin will parse a string of selected text and work out what i18n method to encase the string in.

The plugin makes one main assumption that if the text is encased in single or double quotes - it assumes it's a string being used in php code and as such we don't want to echo or print the string

<h1>Typical Uses</h1>

<b>Normal text</b>
```
Follow the yellow brick road
```

`ctrl + shift + d` will become...

```
<?php _e( 'Follow the yellow brick road' ); ?>
```

<b>Normal text in quotes</b>
```
'Follow the yellow brick road'
```

`ctrl + shift + d` will become...

```
__( 'Follow the yellow brick road' )
```

<b>Normal text with escape</b>
```
Follow the yellow brick road
```

`ctrl + shift + e` will become...

```
<?php esc_html_e( 'Follow the yellow brick road' ); ?>
```

<b>Normal text in quotes with escape</b>
```
'Follow the yellow brick road'
```

`ctrl + shift + e` will become...

```
esc_html__( 'Follow the yellow brick road' )
```
<b>Normal text with attribute escape</b>
```
Follow the yellow brick road
```

`ctrl + shift + a` will become...

```
<?php esc_attr_e( 'Follow the yellow brick road' ); ?>
```

<b>Normal text in quotes with attribute escape</b>
```
'Follow the yellow brick road'
```

`ctrl + shift + e` will become...

```
esc_attr__( 'Follow the yellow brick road' )
```

<b>Text with URLs</b>
```
Follow the <a href="http://yellow.com">yellow</a> <a href="#type=brick">brick</a> <a href="http://roads.ie">road</a>
```

`ctrl + shift + d` will become...

```
<?php printf( __( 'Follow the <a href="%1$s">yellow</a> <a href="%2$s">brick</a> <a href="%3$s">road</a>' ), 'http://yellow.com', '#type=brick', 'http://roads.ie' ); ?>
```

<b>Text in quotes with URLs</b>
```
'Follow the <a href="http://yellow.com">yellow</a> <a href="#type=brick">brick</a> <a href="http://roads.ie">road</a>'
```

`ctrl + shift + d` will become...

```
sprintf( __( 'Follow the <a href="%1$s">yellow</a> <a href="%2$s">brick</a> <a href="%3$s">road</a>' ), 'http://yellow.com', '#type=brick', 'http://roads.ie' )
```

<b>Text with URLs and escaping</b>
```
Follow the <a href="http://yellow.com">yellow</a> <a href="#type=brick">brick</a> <a href="http://roads.ie">road</a>
```

`ctrl + shift + e` will become...

```
<?php printf( esc_html__( 'Follow the <a href="%1$s">yellow</a> <a href="%2$s">brick</a> <a href="%3$s">road</a>' ), 'http://yellow.com', '#type=brick', 'http://roads.ie' ); ?>
```

<b>Text in quotes with URLs and escaping</b>
```
'Follow the <a href="http://yellow.com">yellow</a> <a href="#type=brick">brick</a> <a href="http://roads.ie">road</a>'
```

`ctrl + shift + e` will become...

```
sprintf( esc_html__( 'Follow the <a href="%1$s">yellow</a> <a href="%2$s">brick</a> <a href="%3$s">road</a>' ), 'http://yellow.com', '#type=brick', 'http://roads.ie' )
```

<b>Text with URLs and attribute escaping</b>
```
Follow the <a href="http://yellow.com">yellow</a> <a href="#type=brick">brick</a> <a href="http://roads.ie">road</a>
```

`ctrl + shift + a` will become...

```
<?php printf( esc_attr__( 'Follow the <a href="%1$s">yellow</a> <a href="%2$s">brick</a> <a href="%3$s">road</a>' ), 'http://yellow.com', '#type=brick', 'http://roads.ie' ); ?>
```

<b>Text in quotes with URLs and attribute escaping</b>
```
'Follow the <a href="http://yellow.com">yellow</a> <a href="#type=brick">brick</a> <a href="http://roads.ie">road</a>'
```

`ctrl + shift + a` will become...

```
sprintf( esc_attr__( 'Follow the <a href="%1$s">yellow</a> <a href="%2$s">brick</a> <a href="%3$s">road</a>' ), 'http://yellow.com', '#type=brick', 'http://roads.ie' )
```
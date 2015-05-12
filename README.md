# wp-localize
Sublime Text plugin that localizes a selected string using the WordPress i18n translation methods.

This plugin will parse a string of selected text and work out what i18n method to encase the string in.

Typical cases;

<b>Normal text</b>
Follow the yellow brick road

will become...

```
<?php _e( 'Follow the yellow brick road' ); ?>
```

<b>Text with URLs</b>
Follow the <a href="http://yellow.com">yellow</a> <a href="#type=brick">brick</a> <a href="http://roads.ie">road</a>

will become...

```
<?php printf( __( 'Follow the <a href="%1s">yellow</a> <a href="%2s">brick</a> <a href="%3s">road</a>' ), 'http://yellow.com', '#type=brick', 'http://roads.ie' ); ?>
```
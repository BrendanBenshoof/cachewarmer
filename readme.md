Python Hypertext Markup
=======================

I've developed a hobby of developing prototypes of bad programming languages. PyHP is a fruit of that effort.

PyHP is a low proformance fast development webapp  language. It might be good for prototyping or personal tool development.

Usage is simple, in an HTML file open a `<?` tag, code in python then close with a `?>` tag.

Use the `write(String)` function to output inline into the HTML file.

	<html>
	<body>
	<b>
	<?
	write("Hello world")
	?>
	</b>
	</body>
	</html>

Aguments (post and get) are availible by the `args` dict.
The global `out` is used to hold the output of a block.
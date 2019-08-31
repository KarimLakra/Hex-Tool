<h2><b>A tool for Intel HEX file using python3</b></h2>

<p>
	This GUI is made using tkinter module, it is adapted to work both on Linux and Windows.</p>
</p>
<p>
	This tool is used for devices manufacturing, it needs a .hex file as input, where two lines containing device serial number and MAC address needs to be changed and a new serial and MAC will be inserted to generate a new .hex file, which will allow to program many devices with the same .hex code but different serials and MACs.
</p>
<p>
	The user enters a path to the source file, the source serial number and MAC address (note that if a wrong information is provided, such as Source serial or Source MAC address, the generated file can malfunction even generated correctly)
</p>
<p>
	The output file (or destination file) will be a copy of the Source(without affecting the source file) with a new serial and MAC.
</p>

<p>
<b>GUI Description From Top to Bottom:</b>
<ul>
	<li>The menu contains File->Quit, and Help->About with not much information, but it is there just in case of a further development.</li>
	<li><b>A tool bar that allow the user to:</b>
		<ul>
			<li>save the configuration to minimize the typo mistakes. This option when used for the first time, a config file will be generated, to store the paths, Serial numbers and MACS, an empty field can also be saved empty.</li>
			<li>load config, if the is one already saved, otherwise nothing will be loaded.</li>
			<li>delete the config.</li>
			<li>clear all fields.</li>
		</ul>
	</li>
	<li>the input fields are necessary to generate the files, and a folder buttons to open the source file, and open to destination folder where the files will be saved when generated. Any important filed left empty, an error will be showen in the satatus bar in the bottom.
	<li>two buttons to automatically decrement/increment the destination file serial number and MAC(I linked the buttons to the generate function to generate the destination file, so the user just press Save to save it).
	<li>Generate new button to generate a new hex file(Note that the script create a new file if it dosen't exist, or overwrite it if it exists already without the user interaction, I find the popup dialog boxes annoying specially if you are generating many files. so I made the operation silent).
	<li>two list boxes displaying the modified lines, by double clicking on a line you get information in a box on the right about what each part of the line and what it means with a checksum verification.
	<li>Finally a status bar that interact with the user, it is useful to display errors and successful operation, the bar is painted with different color each time an new operation happens.
</ul>
</p>
<p>
A Special Thanks to Thomas Fischl from his website I copied the script to generate a checksum, he made a useful "HEX file checksum online calculator", and https://stackoverflow.com community which is the best place for every step for programmers.

</p>
References:

  <a href="https://www.fischl.de/hex_checksum_calculator/">hex checksum calculator</a>
  
  <a href="https://en.wikipedia.org/wiki/Intel_HEX">Intel HEX</a>

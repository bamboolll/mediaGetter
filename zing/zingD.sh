#!/bin/sh

outDir="../tmp"
url=$1
album=$2
echo "url is $url"
echo "output folder: $album"
out1="${outDir}/album.html"
out2="${outDir}/lines"
out3="${outDir}/lines.links"

#Step 1: Download HTML 
lynx -source $url > $out1
#Step 2: Parse for link line
cat $out1  | sed 's/<\/a>/\n/g' | grep music-download > $out2
#Step 3: Parse for links and names and put to file
rm -rf $out3
while read line 
do
	link=$( echo $line | sed 's/<a href="\([^"]*\)".*/\1/g' );
	name=$( echo $line | sed 's/.*title="Download \([^"]*\)".*/\1/g' );
	echo "link-${link}:name-${name}" >>$out3;
done < $out2;
#Step 4: Download file
rm -rf ${album};
mkdir ${album};
while read line
do
	link=$( echo $line | sed 's/link-\(.*\):name-.*/\1/g' );
	name=$( echo $line | sed 's/.*:name-\(.*\)/\1/g' ); 
	#fix space in name
	name=$( echo $name | sed 's/ /./g' );
	echo "Downloading ${name} ....";
	wget ${link} -O "${album}/${name}.mp3";
done < $out3;






# Anzhc-s-Dataset-Processing-Tools
Tools i've created(likely all of them will be with GPT4 usage) for processing and possible enchancement of dataset tagging
## Tag Filtering v2  
Uses roughly 780k tags from Danbooru, split in to 5 different lists, which you can choose to, or not to, delete.  
Utilizes 3 stages of filtering, main filtering, removing tags that are in huge lists, additional filtering, which does pass with v1 tag list, and outliers removal, which let you choose to get rid of tags that are not present in any of those lists. This helps to reduce unwanted tags to minimum, and saves your sanity.  
TAG FILES ARE NOT INCLUDED, AS THEY CURRENTLY CONTAIN LINKS, WHICH GITHUB WOULD NOT LIKE, FROM WHAT I CAN TELL, PLEASE, DOWNLOAD THEM FROM CIVITAI ARCHIVE - https://civitai.com/models/99328/tag-filtering-v1v2  
#### Changelog  
v2.5 - drastic performance increase due to utilization of sets instead of lists(thanks random guy from Civitai for suggesting that).  
## Tag Filtering
It uses WD1.4 Tagger list of tags(~11k tags) that i went through and removed tags i think are not important. You will likely disagree, and for that i've included referance tag list for you to go over them yourself. Feel free to request pulls with your own versions.
I will especially appreciate if someone will go over full Danbooru tag list from DeepDanbooru tagger(over 100k tags).

I am including 2 modes: Unwanted and Wanted tags.

In Unwanted mode it will remove tags that are specified in respective list.
In Wanted mode it will remove all, but tags that are specified in respective list. Use this for scraped images. (Keep in mind that it will remove almost all japanese tags as well, as i don't know meaninig of 95% of them)

There are 3 general options to each of them:

SFW(0) - removes most NSFW tags as well, this is useful, if you train SFW dataset, but fear that autotagger could imagine something lewd.
NSFW(1) - removes(or keeps in Wanted mode) tags, but excludes NSFW tags as well.

Data duplication(2) - Removes redundant tags, that are often present. For example:

If you have shirt and white shirt in the same image, it will remove shirt tag, as it's redundant. It works only on exactly matching words in tags, and it doesn't work on the tags of the same power, so your multi-character images are safe, it will not remove red shirt if it's present in the same image with the white shirt.

Keep in mind that Mode(2) is always on, and will be working alongside tag remove in modes 0 and 1.

Just use relevant .bat file to launch one or other mode.

## Brightness Tagger  
Lil script that splits images into multiple categories of brightness, with normal brightness being not tagged.  
It does add tag at the end.  

It does work quite decent from what i see, but it is yet to be seen if it has real use for particular SD models. Did not show significant change on XL so far.  
Likely will be useful for 1.5, as it can go dark a bit, and will likely be very useful for SD3, as it confirmed can go dark.

## Half-assed color-theme tagger
*Future

## Semi-reliable Complexity Tagger
*Future

## Suggestions
If you have any ideas for processing to get useful tags reeliably, please share, and i'll try to implement that tool.

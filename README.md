# Anzhc-s-Dataset-Processing-Tools
Tools i've created(likely all of them will be with GPT4 usage) for processing and possible enchancement of dataset tagging
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


## Suggestions
If you have any ideas for processing to get useful tags reeliably, please share, and i'll try to implement that tool.

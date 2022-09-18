# pwrtraincolour
Gather a dataset for training/testing a colour recognition algo./ai using a BH1745 and an AS7262 sensor

Curently only the data capture and training data generator programs done to a basic extent

the implementation of colour name lookup could be any number of ai techniques but I prefer fuzzy logic as you can see where fuzzy logic went wrong but that's not so easy with other methods.

And I think fuzzy logic is suitable for this problem, along with candidate selection and majority decision

my basic method is done in the data collection/training prog which is the percentage of the total sensors signal in each bin for each colour

But I think the data gathered by these two progs will be useful for any method.

It seems to me key for any good algo/ai is a good data set... the old addage... garbage in, garbage out.

If anyone wants to post their working solutions to the lookup problem based on this data I will be interested, raise an issue.

You will have to discover a lot of the subtleties yourself, such as not casting shadows etc. or accounting for such things.

using the illuminators provided will probably eliminate some of those problems but introduce subtleties of its own, like probably accentuating angle effect.

On the topic of whether the as band they called violet on the AS7262  should be called indigo, I think it should, violet is 380-420, the centre frequency is 450 for band 6, BUT the trend seems to be to deny Sir Isaac Newton as Indigo does not even exist in the X11 colour list, Newton thought he could see seven colours after a prism had split it so I take his word for it.  When I looked on the internet I thought raw indigo looked a deep purple/blue but i am seeing it through a cheap monitor using the rgb colour model.

but then the modern science of colour is fooling the eye with rgb eh!  as for the cmyk dotted print layers, thats amazing!  (The modern science of science is fooling people with statistics???)
       
And funny that the old dye for violet (roman purple) was sea snails in vast quantities.  And funny that Indigo had to be converted to “Indigo White” before used to dye many shades of blue LOL

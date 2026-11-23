<!-- docs/adr/2026-10-25-kathryn-flinn-19-storage-rfc.md -->

# RFC: Data Storage Solution

<!-- Decision record header. Leave Status as "Proposed" until your team decides,
     before or after the reviews. Then fill in the outcome and the decision date.
     The document stays where it is; this header is what makes it a record. -->

| Field | Value |
| --- | --- |
| Author | Kathryn Flinn |
| Date | 2026-10-25 |
| Status | Accepted |
| Decision Date | 11/16/2026 |
| Deciders | Kathryn Flinn, Julie Feldhousen, Jae Grunwald, and Adison Daggett |
| Superseded By | (link, if applicable) |

## Problem and Context

Our Capstone project is to develop a tool that displays species habitat maps for the Oregon Department of Fish and Wildlife. The maps are to be a synthesis of range maps created by habitat experts, as well as deductive rules used to narrow down the probable places where a given species would be found. The intention is that this tool includes a way to edit deductive rulesets used to generate maps, as well as a way to modify which layers are used to determine where a species may be found. 

To create maps from deductive habitat rules, this project needs extensive data on habitat features such as elevation, water features, and land cover. This data is very large. The total size of the unclipped data for the hydrography (i.e. water features) layer alone is just over 70 gigabytes for the entire United States [7]! The size of this data, therefore, poses a distinct challenge in its management. One of the driving goals of our project is that it is accessible: it should be easy to use, and there should not be significant barriers to someone wanting to use the tool. But if someone had to download all of the data required to use this tool, the sheer amount of storage required could pose a barrier to the accessibility of our tool.

Therefore, our team needs to decide on a way to manage habitat data. If we do not make a decision now, then our team will lack a way to organize the large amount of data needed for our project. As a result, we would have to rely on individuals downloading the several gigabytes of data needed to run the tool, which may limit its accessibility. Furthermore, choosing the wrong data solution could lead to poorer performance over time, which, again, could limit the usability and accessibility of the tool.

## Options

### Option A. Remotely Hosted PostgreSQL Database
A remotely hosted PostgreSQL database offers one way that we could organize the data. This option could be useful for organizing multiple types of data. The data layers used for elevation, water features, and land covers are in binary .adf files, which Postgres can handle. Postgres can store these files as byte streams, or as whole objects called Large Objects. Therefore, Postgres would offer a way to store multiple types of data while organizing the data such that SQL queries could be used to efficiently retrieve different combinations of the data. 

However, PostgreSQL would have a cost: namely, the cost of hosting the database remotely. Amazon's RDS for Postgres would offer a way of doing this for $0.115 per gigabyte per month [1]. To reduce costs, we could limit stored data to just data related to the northwest region of the United States, as most of the data layers are naturally split up by region. A conservative estimate of our required data storage would be approximately 20 gigabytes; consequently, we would be looking at a monthly cost of roughly $2.30 per month, or about $27.60 per year. While this is not a huge sum of money, the Project Partner has indicated that he would prefer a storage solution that does not have a monetary cost associated with it.

Another concern is performance issues from storing large files in Postgres. According to the Postgres wiki, storing files that are larger than 100 megabytes --- and our data layers would be larger than 100 megabytes each --- can cause performance issues [2]. As noted previously, performance issues could lessen the accessibility of our tool, which limits its usability and helpfulness.

### Option B. Cloud Storage
Using stand-alone cloud storage, such as DigitalOcean's Network File Storage (NFS), would be an alternative to a traditional database. With NFS, we could store our data layers directly in the cloud, in a file system-like format. Given that our data layers may comprise several different files that all must be accessed and used at once, being able to organize our files into folders would be very helpful. This could also be more intuitive than using a traditional database. Another positive aspect of NFS is that it is built to handle large amounts of data, and thus would not see the same type of performance issues that a traditional database might see with the same file sizes. 

Of course, this would also have a cost, which would be higher than that of AWS's RDS for Postgres. Under DigitalOcean's NFS, it would cost approximately $0.15 per gigabyte per month for the standard performance tier; if we use only store data for the northwestern region of the United States and thus use the estimate of 20 gigabytes of data, this translates to $3 per month or $36 per year [3]. This is more expensive than the RDS for Postgres option, and so cost becomes a greater concern. And, as mentioned before, any option with an ongoing cost is not ideal.

### Option C. Reduce Data Size but Still Require Manual Downloads
We could also look into ways to reduce the data size down to a more acceptable size. For instance, clipping the data to the state of Oregon alone, instead of storing all data for the northwestern United States, could significantly reduce the amount of data needed to run the program. Additionally, such a method would not detract from the functionality of our tool, as we are only generating maps for the state of Oregon; therefore, we do not need data from states outside of Oregon. We could also investigate alternative data formats that are more space-efficient; for instance, Zarr, GeoTIFFs, and HDF5 file formats all support internal compression, which would allow for greater storage efficiency [4], [5], [6].

This option would require additional work from the team: namely, editing the data layers and possibly converting the data to an alternative format. However, the data clipping and transformation would be a one-time operation; once the data has been clipped and adjusted to a more space-efficient format, we would not need to edit the data in the future. Therefore, no work would be required for maintaining our data. 

One of the most appealing aspects of this option, however, is that it has no monetary cost. The database and cloud storage options would require continual payments, while this option has no monetary cost whatsoever.

The drawback, however, is that users would still be required to download some amount of data. Therefore, users with exceedingly limited storage may not find our tool accessible under this option.

### Option D. Do Nothing
Doing nothing in this case would mean relying on the users to download the full data layers themselves. Again, we could reduce data to just the northwestern United States to reduce data storage requirements; however, it would still mean that users would be required to download an estimated 20 gigabytes of storage. 

To make the data accessible to users, we could compile the data in zip files in an accessible online storage drive, such as OneDrive. While this option would mean minimal work and cost for our team, it would put the burden of storage and data organization on the user. This would make our application less accessible and harder to use, which would ultimately reduce its effectiveness and usage.

## Analysis
Cost, performance, and accessibility are the major technical tradeoffs at play in this decision. If we prioritize cost in terms of both monetary cost and team labor, we could choose to do nothing; this would require very little work from the team. However, users would be forced to personally download an estimated 20 gigabytes of data to use our tool. This may be unappealing to many, as this would be a considerable storage requirement. As a result, offloading the burden of data storage to the user may lead to less people using our tool, which means our main goal of accessibility would not be accomplished.

Prioritizing performance and accessibility often go hand-in-hand, as a more performant tool would be more appealing and accessible to users. However, accessibility does not always imply performance; for instance, while using a remote Postgres database would remove the burden of data storage from the user, it still may not be the most performant choice: as mentioned above, the Postgres wiki states that files larger than 100 megabytes could result in poor database performance [2]. When we consider the fact that most files in our data layers exceed this limit, it becomes clear that performance may still suffer, despite the improvements in accessibility. Additionally, this option has an ongoing monetary cost, which, at a conservative 20 gigabyte  storage estimate, would be $27.60 per year [1]. As a result, a remotely hosted Postgres database may not be the ideal storage solution for our data.

The Network File Storage, on the other hand, would be more performant than a remotely hosted Postgres database. However, its performance would come at a monetary cost, and our team's Project Partner would prefer to avoid any such monetary cost. Recall that, at an estimated 20 gigabytes of storage, this solution would require an annual payment of $36 [3]. For as long as we want the tool to use data in the cloud, we would have to pay for it. This would conflict with the Project Partner's preferences for a no-cost tool that requires little maintenance. 

Clipping the data layers and modifying their file formats would be cost-effective, performant, and accessible. It is cost-effective in that it has no monetary cost; we would not have to pay for remote hosting solutions. Additionally, based on preliminary data clipping by Julie Feldhousen, data clipping is highly effective at reducing the size of the data. For instance, the hydrography layer was originally just over 70 gigabytes in total, with about 9.5 gigabytes of that being for the northwestern United States [7]. However, this data layer was successfully reduced to just over one gigabyte in size after the data was clipped to the state of Oregon alone [7]. Consequently, data clipping would make our tool more accessible by lessening the amount of storage a user must have access to. Choosing a suitable file format that supports internal compression could also encourage higher performance when reading the data; further, requiring the data to exist locally would reduce any network latency that would exist with remote or cloud options, which again would boost performance. Again, the drawback would be that users would be required to download some data, which may limit its accessibility for users with very limited storage.

## Recommendation and Verification Plan
My recommendation is that we simply clip the data layers and modify the data file formats as needed. As mentioned above, limited data clipping done by Julie Feldhousen has shown that the method is highly effective at reducing the size of the required data layers. The hydrography layer is one of the largest data layers required by our tool; therefore, its size reduction from 9.5 gigabytes for the northwestern United States to only 1 gigabyte for Oregon suggests that the total data requirement for all 11 clipped layers could be 5-10 gigabytes, if we assume that each of the other clipped data layers is no bigger than the clipped hydrography layer [7]. This data requirement is smaller than the conservative 20 gigabyte requirement of the unclipped data, meaning that it would reduce the storage burden significantly.

Additionally, by choosing a data file format such as GeoTIFFs, HDF5, or Zarr, we could reduce the size of the clipped data even more, since these file formats support internal compression [4], [5], [6]. They are also well-suited for the geospatial data we would be dealing with, meaning that choosing such a data format could lead to our tool being more performant [4], [5], [6].

The other major appeal to this option is its lack of monetary cost. According to the project partner, we are aiming to develop a tool that has little maintenance cost --- both monetary and otherwise. Because this option would not require us to remotely host the data, there would not be any ongoing monetary cost for someone maintaining the tool. 

There are two aspects that need to be verified, however: the final data storage burden and the correctness of the clipped data. To confirm the former aspect, we would simply sum the total storage sizes of each clipped and converted data layer to make sure it falls within an acceptable size range --- for example, 5 to 10 gigabytes. This would allow us to verify that the storage burden we are imposing on the user is not significant enough to impact the accessibility of our tool. We could also survey the users of our tool --- i.e., workers at ODFW --- to ensure that our data requirement is not great enough to prevent them from using it. The exact range of an acceptable data burden, therefore, would need to be confirmed with ODFW through our Project Partner. The latter aspect would take more testing, however. Put simply, converting our data layers to another file format could require data manipulation that runs the risk of accidental corruption or mistakes. Therefore, it would be necessary to generate maps of each converted data layer and compare them to their original data layer's generated map; maps that match are demonstrably correct, while maps that don't match suggest that the converted layer contains incorrect or corrupted data.

## Constraints
I do not believe there are any constraints in regards to licensing, data usage, IP, or partner confidentiality for this decision. The data that would be stored by our data management solution would be publically available information, so security and confidentiality are not of particular concern. The only concrete constraint is the Project Partner's preference to use a free storage solution to eliminate any monetary cost associated with maintaining the tool long-term. 

## Delegation and Validation
Nothing was given to AI for this assignment, as I felt that AI assistance in my research and writing were unnecessary. Therefore, all research and writing was completed by me.

## Decision
Accepted: Option C was agreed upon by all group members, and was approved by the Project Partner. Therefore, the data layers required for the project will be clipped to the state of Oregon alone, with the data being converted from .adf files to GeoTIFFs. This file format was chosen because, as stated above, it supports internal compression and thus would help further reduce the storage burden. Additionally, this data conversion can be performed automatically by ArcGIS during the data clipping, meaning that there is little developer overhead other than the time needed to clip the data itself. Additionally, because the data conversion is performed by ArcGIS directly, there is less of a chance that the converted data layers will contain errors or be corrupted. Of course, this is still a possibility; therefore, it would still be helpful to compare the visualized GeoTIFF files with the original files.

## Bibliography
[1] “Amazon RDS for Postgresql Pricing.” Amazon, aws.amazon.com/rds/postgresql/pricing/. Accessed 7 Nov. 2026. 
[2] “Binary Files In DB.” PostgreSQL Wiki, 5 May 2021, wiki.postgresql.org/wiki/BinaryFilesInDB. Accessed 7 Nov. 2026.  
[3] “Network File Storage.” Digital Ocean, www.digitalocean.com/pricing/network-file-storage. Accessed 21 Nov. 2026. 
[4] “Optimized GeoTIFFs.” Cloud-Optimized Geospatial Formats Guide, guide.cloudnativegeo.org/cloud-optimized-geotiffs/intro.html. Accessed 16 Nov. 2026.
[5] Wasser, Leah A. “Hierarchical Data Formats - What Is HDF5?” NSF | Neon, 2 Apr. 2026, www.neonscience.org/resources/learning-hub/tutorials/about-hdf5.
[6] “Zarr.” Cloud-Optimized Geospatial Formats Guide, guide.cloudnativegeo.org/zarr/intro.html. Accessed 7 Nov. 2026.
[7] Flinn, Kathryn. "Hydrography Layer Data Sizes." OneDrive, 22 Nov. 2026, https://oregonstateuniversity-my.sharepoint.com/:f:/g/personal/flinnk_oregonstate_edu/IgBJm5jHqKsXT64wTuUxI1YQAcOdKJ0eKSqfX4KCsjDj-hY?e=DixKNb.
<!-- docs/adr/2026-10-25-kathryn-flinn-19-storage-rfc.md -->

# RFC: Data Storage Solution

<!-- Decision record header. Leave Status as "Proposed" until your team decides,
     before or after the reviews. Then fill in the outcome and the decision date.
     The document stays where it is; this header is what makes it a record. -->

| Field | Value |
| --- | --- |
| Author | Kathryn Flinn |
| Date | 2026-10-25 |
| Status | Proposed |
| Decision Date | (fill when decided) |
| Deciders | (who agreed to the outcome) |
| Superseded By | (link, if applicable) |

## Problem and Context

Our Capstone project is to develop a tool that displays species habitat maps for the Oregon Department of Fish and Wildlife. The maps are to be a synthesis of maps created by habitat experts, as well as deductive rules used to determine the probable places where a given species would be found. The intention is that this tool includes a way to compare and contrast maps created by different experts and those created using deductive habitat rules. 

To create maps from deductive habitat rules, this project needs extensive data on habitat features such as elevation, water features, and land cover. This data is very large, even when limited to just the Pacific Northwestern region of the United States. The size of this data, therefore, poses a distinct challenge in managing the data. One of the driving goals of our project is that it is accessible: it should be easy to use, and there should not be significant barriers to someone wanting to use the tool. But if someone had to download all of the data required to use this tool, the sheer amount of storage required could pose a barrier to the accessibility of our tool.

Therefore, our team needs to decide on a way to store habitat data so it could be fetched for use in our tool. If we do not make a decision now, then our team will lack a way to organize the large amount of data needed for our project. As a result, we would have to rely on individuals downloading the several gigabytes of data needed to run the tool, which may limit its accessibility. Furthermore, choosing the wrong data solution could lead to poorer performance over time, which, again, could limit the usability and accessibility of the tool.

## Options

### Option A. Remotely Hosted PostgreSQL Database
A remotely hosted PostgreSQL database offers one way that we could organize the data. This option could be useful for organizing multiple types of data, not just simple, standardizable data like species observations. The data layers used for elevation, water features, and land covers are in binary .adf files, which Postgres can handle. Postgres can store these files as byte streams, or as whole objects called Large Objects. Therefore, Postgres would offer a way to store multiple types of data while organizing the data such that SQL queries could be used to efficiently retrieve different combinations of the data. 

However, PostgreSQL would have a cost: namely, the cost of hosting the database remotely. Amazon's RDS for Postgres would offer a way of doing this for [$0.115 per gigabyte per month](https://aws.amazon.com/rds/postgresql/pricing/). A conservative estimate of our required data storage would be approximately 20 gigabytes, while a larger estimate would be up to 50 gigabytes; consequently, we would be looking at a monthly cost of anywhere from $2.30 to $5.75 per month, or about $27.60 to $69 per year. While this is not a huge sum of money, there is still the question of who would pay for this storage, and whether such an annual cost would be acceptable.

Another concern is performance issues from storing large files in Postgres. According to the Postgres wiki, storing files that are larger than 100 megabytes --- and our data layers would be larger than 100 megabytes each --- can cause performance issues. As noted previously, performance issues could lessen the accessibility of our tool, which limits its usability and helpfulness.

### Option B. Cloud Storage
Using stand-alone cloud storage, such as DigitalOcean's Network File Storage (NFS), would be an alternative to a traditional database. With NFS, we could store our data layers directly in the cloud, in a file system-like format. Given that our data layers may comprise several different files that all must be accessed and used at once, being able to organize our files into folders would be very helpful. This could also be more intuitive than using a traditional database. Another positive aspect of NFS is that it is built to handle large amounts of data, and thus would not see the same type of performance issues that a traditional database might see with the same file sizes. 

Of course, this would also have a cost, which would be higher than that of AWS's RDS for Postgres. Under DigitalOcean's NFS, it would cost approximately $0.15 per gigabyte per month for the standard performance tier; if we use 20 gigabytes, this translates to $3 per month or $36 per year, but if we use 50 gigabytes per year, the cost would jump to $7.50 per month or $90 per year. This is more expensive than the RDS for Postgres option, and so cost becomes an even greater concern.

### Option C. Do Nothing
Doing nothing in this case would mean relying on the users to download the data themselves. To reduce the burden as much as possible, we could compile the data in zip files in an accessible online storage drive, such as OneDrive. While this option would mean minimal work and cost for our team, it would put the burden of storage and data organization on the user. This would make our application less accessible and harder to use, which would ultimately reduce its effectiveness and usage.

## Analysis
Cost, performance, and accessibility are the major technical tradeoffs at play in this decision. If we prioritize cost, we would choose to do nothing; but then, users would be forced to personally download around 20 gigabytes of data to use our tool. This may be unappealing to many, as 20 gigabytes is a considerable storage requirement. As a result, offloading the burden of data storage to the user may lead to less people using our tool, which means our main goal of accessibility would not be accomplished.

Prioritizing performance and accessibility would go hand-in-hand, as a more performant tool would be more appealing, and more accessible, to users. However, accessibility does not always imply performance; for instance, while using a remote Postgres database would remove the burden of data storage from the user, it still may not be the most performant choice: as mentioned above, [the Postgres wiki](https://wiki.postgresql.org/wiki/BinaryFilesInDB) states that files larger than 100 megabytes could result in poor database performance. When we consider the fact that most files in our data layers exceed this limit, it becomes clear that performance may still suffer, despite the improvements in accessibility.

However, performance often comes at a monetary cost, and I am unsure what monetary cost could be covered by our team's Project Partner. The pricing estimates referenced in the [Cloud Storage](#option-b.-cloud-storage) section are somewhat high, as they are anywhere from [$36-$90 per year](https://www.digitalocean.com/pricing/network-file-storage) at the standard performance tier. This concern is especially significant when we consider the fact that the cost (and maintenance) of a cloud solution would be ongoing; essentially, for as long as we want the tool to use data in the cloud, we would have to pay for it. As a result, more conversation with our Project Partner may be necessary before a concrete decision could be made.

## Recommendation and Verification Plan
My recommendation is that DigitalOcean's Network File Storage (NFS) is used. While pricier than AWS's RDS for Postgres, it is built for handling files and would thus be the most performant option of the three proposed. By removing the burden of data management from the user, and by providing a high-performance option for storing and accessing files remotely, we would enhance the usability and thus accessibility of our application.

Proving accessibility here would mean proving that the user is not responsible for downloading and organizing data layers. As long as we store data remotely and have our application fetch it, rather than the user, we can consider our solution to be accessible. One other aspect of accessibility would be uptime, which can be monitored using [built-in tools](https://docs.digitalocean.com/reference/api/reference/uptime/) from DigitalOcean. This is a metric that will need to be discussed with our Project Partner, as I am unsure what uptime is required and thus what an acceptable metric would be. This is a metric that would be checked continually for the first month to confirm an acceptable uptime; however, it should be continually monitored over the course of the NFS's usage to make sure that it maintains a high uptime over time.

To prove that our chosen solution is performant, however, we would also need to test how quickly data layers could be retrieved from the NFS. I am still unsure what an acceptable amount of time would be; this is something that would need to be agreed upon with our Project Partner. This metric would be checked after uploading our data to the NFS, however, so that performance could be confirmed before the application's deployment.

## Constraints
I do not believe there are any constraints in regards to licensing, data usage, IP, or partner confidentiality for this decision. The data that would be stored by our data management solution would be publically available information, so security and confidentiality are not of particular concern.

## Delegation and Validation
Nothing was given to AI for this assignment. All research and writing was completed by me.

## Decision
Proposed, pending the team's decision.
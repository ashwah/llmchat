# Birkett Long - Content Migration - Documentation

## Introduction

This document serves as a comprehensive guide for migrating content to a brand new Drupal 10 website for Birkett Long. It outlines the entire process of importing staff pages, various content types, and associated media from the client's existing website. The goal is to seamlessly populate the new Drupal 10 site with relevant information while ensuring it adheres to the established design guidelines. Additionally, the migration aims to update internal links within the content wherever new URLs are provided, promoting a smooth user experience on the revamped website.

This documentation is primarily intended for Drupal developers with a solid understanding of the Migrate API and best practices for Drupal development. Familiarity with the source data structure and the client's specific content requirements is also beneficial.

By following the steps outlined in this guide, developers can effectively import content, transform it to match the new website's design, and establish proper internal linking within the migrated content. This will ensure a well-structured and user-friendly Drupal 10 website for Birkett Long.

## Deployment Steps

The migration process for the client's Drupal 10 website aims for simplicity and efficiency. By grouping together various migration scripts, executing the migration becomes a straightforward task. Using a single Drush command, the migration code is deployed and the migration process is initiated, seamlessly integrating with the Bitbucket pipeline workflow. This streamlined approach minimizes complexity and ensures a smooth transfer of content to the new environment.

### Deployment Steps

**Bitbucket Pipeline:**
- Trigger the standard Bitbucket pipeline process to deploy migration code.
- Ensure migration scripts and configurations are included.

**Migration Execution:**
- Run migration process using Drush command: `drush mim --group=bl`.
- Monitor for errors and warnings during migration.

**Validation:**

Verify the following content types are populated: 
- People 
- Blogs 
- Case Studies 
- Flexible Pages

Confirm taxonomy vocabs:
- Glossary 
- Categories

Media entities:
- Images
- Remote video

Also check the content of page. Ensure that the page title matches the body of the page. Also check that some link replacements have been made (altho it isn't possible to update ALL links). 

You could also compare the spreadsheet to the pages. If you do, you can also check incorrect links. If an incorrect link is found, you should look-up that link in the URL column of the "m-ALL" tab of the spreadsheet. Hopefully you will confirm that that link doesn't exist on the sheet, and therefore is not a link that is possible to update.





## Data Preparation

### Staff Data 

The staff data is provided in a single tab within the spreadsheet provided by the client. This data does not require any manipulation and can be imported as-is into the Drupal database.

### Page Data

The page data is contained within multiple tabs in the provided spreadsheet. Not all tabs are intended for import; specifically, the tabs labeled "Events Archive," "Events Modules," "Uncrawled Pages," and "Blocks" are excluded from the import process.

#### Glossary Vocabulary

The "Glossary (Global)" tab is to be imported into the Glossary vocabulary in Drupal. No preparation is required for this tab, as it can be used as-is for the import process.

#### Page Types Preparation

To prepare the remaining tabs for import, additional tabs need to be created and populated as follows:

1. **Create Tabs:** 
    - Create tabs named 'm-ALL', 'm-FLEXIBLE', 'm-CASE STUDIES', and 'm-BLOGS'.
    - Copy the headings from the original 'Misc' tab into these new tabs.

2. **Add Columns:** 
    - Add two columns at the left side of each new tab: 'Page type' and 'ID'.
    - The 'Page type' column is used to designate the type of page being imported.
    - The 'ID' column is used to create a consistent index for the page content.

3. **Copy Data to 'm-ALL' Tab:**
    - Copy data from each of the following tabs into the 'm-ALL' tab: 'Misc', 'Sectors', 'Services', 'Careers', 'Case Studies', 'Testimonials', 'Blog', 'Library', 'Glossary (Local)', and 'Contact'.
    - Add the corresponding page type in the "Page type" column for each imported tab.
    - Fill the 'ID' column with incrementing integers to create unique identifiers for the page content.

4. **Distribute Data to Other Tabs:**
    - Copy data from the 'm-ALL' tab to the relevant migration tabs.
    - For the 'm-FLEXIBLE' tab, copy data from 'Misc', 'Sectors', 'Services', 'Careers', 'Testimonials', 'Library', 'Glossary (Local)', and 'Contact' tabs.
    - For the 'm-CASE STUDIES' tab, copy data from the 'Case Studies' tab.
    - For the 'm-BLOGS' tab, copy data from the 'Blog' tab.

The original "Pages.xls" sheets (excluding "Glossary (Global)") will not be directly used for migration. Data will be processed and transformed within the additional sheets so that the relevant entities types can be created for each.


## Migration Script Overview

The migration process is orchestrated through a series of YAML migration scripts, each responsible for migrating specific types of content from the source to the target Drupal 10 website. Below is a list of the migration scripts:

- `migrate_plus.migration.bl_glossary.yml`
- `migrate_plus.migration.bl_pages__blogs.yml`
- `migrate_plus.migration.bl_pages__case_studies.yml`
- `migrate_plus.migration.bl_pages__flexible.yml`
- `migrate_plus.migration.bl_pages_category_terms.yml`
- `migrate_plus.migration.bl_pages_paragraphs_image.yml`
- `migrate_plus.migration.bl_pages_paragraphs_image_files.yml`
- `migrate_plus.migration.bl_pages_paragraphs_image_media_entities.yml`
- `migrate_plus.migration.bl_pages_paragraphs_video.yml`
- `migrate_plus.migration.bl_pages_paragraphs_video_media_entities.yml`
- `migrate_plus.migration.bl_pages_paragraphs_wysiwyg.yml`
- `migrate_plus.migration.bl_staff.yml`
- `migrate_plus.migration.bl_staff_image_files.yml`
- `migrate_plus.migration.bl_staff_media_entities.yml`

Each migration script is designed to handle the migration of specific content types or entities, such as glossary terms, blog pages, case studies, staff profiles, and various paragraph types.

### Dependencies

Individual migration scripts may have dependencies, ensuring that migrations run in the correct order to maintain data integrity. Dependencies are specified within each migration script's configuration.

### Grouped Migration

The migration scripts are grouped together for convenience, allowing the entire suite of scripts to be executed with a single Drush command: `drush mim --group=bl`. This command initiates the migration process for all content types associated with the Birkett Long project.

### Post-Migration Processing

Following the execution of the migration scripts, a post-migration event subscriber is triggered. This subscriber performs key processes, including updating links within migrated content if the link destination was included in the pages that were migrated. Notably, this process executes after the `bl_pages__blogs` migration, ensuring that all relevant content has been migrated before link updates are applied.



## Migration Supporting Process

The migration process leverages the tools provided by the Migrate Spreadsheet contrib module, which serves as the foundation for building migrations from spreadsheets. However, to accommodate the unique requirements of our migration, we have extended the behavior of the "iterator" provided by the module.

### Explosion Iterator

In our migration, certain rows in the spreadsheet contain data for more than one destination entity. For example, the "category" column may hold comma-separated strings. To handle this scenario, we have implemented an "Explosion Iterator." Unlike the default iterator, which steps from each row to the next, the Explosion Iterator steps between rows while also stepping between each item in the column designated as the "explode column." This allows us to treat each item in the comma-separated list as a unique entity to import.

### Page Content Handling

Similarly, the content of pages may need to be broken up into different types of paragraphs, such as 'wysiwyg' content, 'image' content, or 'video' content. To facilitate this, we apply the same approach of the Explosion Iterator, treating each section of the page content as a unique entity during the import process.



## Migration Script Details

In this section, we will outline each migration script, corresponding to a YAML file, used in the migration process. Each migration script is responsible for migrating specific types of content or entities from the source to the target Drupal 10 website. We will provide details about the purpose, functionality, and key configuration settings of each migration script.

Additionally, we will group the migration scripts into subsections based on their functionality and associated content types. This organization will help provide a clear understanding of how different parts of the migration process are orchestrated and executed.


### Glossary Taxonomy Term Import

The `migrate_plus.migration.bl_glossary.yml` migration script is responsible for importing data into the Glossary vocabulary as taxonomy terms. It extracts data from the source spreadsheet, mapping the title field to the taxonomy term name and the content field to the term description. A custom processor is used to skip duplicate pre-existing terms (`bl_skip_existing_term`).


### Staff Import

The following migration scripts, executed in the specified order, handle the import of staff data from the staff spreadsheet into the People content type:

1. **`migrate_plus.migration.bl_staff_image_files.yml`**: This script initiates the download of images associated with staff members into file entities in Drupal.
   
2. **`migrate_plus.migration.bl_staff_media_entities.yml`**: Following the image file download, this script creates media entities for the staff images.
   
3. **`migrate_plus.migration.bl_staff.yml`**: The final step in the staff data migration process, this script creates the People content pages in Drupal.

It's important to note that the final step, `bl_staff.yml`, serves as a dependency for the other page scripts, as the other spreadsheets reference members of staff. Additionally, a custom processor (`bl_url_path`) is utilized to format a URL imported into the `field_source_url` field.



### Category Import

The migration script `migrate_plus.migration.bl_pages_category_terms.yml` is responsible for importing data into the "Categories" vocabulary. It utilizes the explosion iterator mentioned earlier to split the content in the "Category Names" field into individual category strings.

This script is designed to extract data from the source spreadsheet and populate the "Categories" vocabulary in Drupal. It handles the splitting of category names into individual strings using the explosion iterator, ensuring that each category is imported as a separate taxonomy term.

In addition, a custom processor (`bl_prevent_duplicate_terms) is incorporated into the migration process to ignore duplicate rows. This helps maintain data integrity by preventing the import of duplicate category terms.


### Image, Image Media Entity, and Image Paragraph Import

These migrations employ an extension of the explosion iterator, utilizing the Content Data field as the explode column. The data is segmented into chunks of content based on its type, whether it's WYSIWYG content, video content, or image content. This segmentation allows for the importation of each type of content into its respective paragraph type.

All these migrations utilize a custom process called 'bl_filter_paragraph_type', which selectively allows only certain types of content chunks to pass through. In this case, the process filters by image content.

1. **`migrate_plus.migration.bl_pages_paragraphs_image_files.yml`**: This migration script is responsible for downloading the image files.

2. **`migrate_plus.migration.bl_pages_paragraphs_image_media_entities.yml`**: Following the image file download, this script creates media entities from the images processed in the previous step.

3. **`migrate_plus.migration.bl_pages_paragraphs_image.yml`**: The final step in the image-related migration process, this script creates paragraphs of type 'image' from the media entities.


### Video and Remote Video Paragraph Import

Similar to the image-related migrations, these migrations utilize the explosion iterator. However, this time, they specifically filter down to the video content using the 'bl_filter_paragraph_type' processor.

1. **`migrate_plus.migration.bl_pages_paragraphs_video_media_entities.yml`**: This migration script creates the media entities directly. Unlike images, which require downloading, the video media entities in this case are remote videos.

2. **`migrate_plus.migration.bl_pages_paragraphs_video.yml`**: This migration script creates the paragraph content of type video.
               

### WYSIWYG Paragraph Import

Similar to previous migrations, this process utilizes the explosion iterator but specifically filters for regular content.

- **`migrate_plus.migration.bl_pages_paragraphs_wysiwyg.yml`**: This migration simply populates paragraphs of type WYSIWYG with the content. 

Note that for WYSIWYG content, the iterator cleans up the HTML tags in line with Drupal's basic WYSIWYG filter.


### Page Import

These migrations utilize the regular spreadsheet iterator and reference their respective tabs in the pages spreadsheet.

- **`migrate_plus.migration.bl_pages__blogs.yml`**
- **`migrate_plus.migration.bl_pages__case_studies.yml`**
- **`migrate_plus.migration.bl_pages__flexible.yml`**

Each migration performs a similar task with slight variations for fields specific to each content type.

Custom processors play a vital role in these migrations:

- **'bl_paragraph_lookup':** Handles the lookup of paragraphs created in previous steps, adding them to the paragraph fields on each page.
- **'bl_first':** Retrieves the first category, used as the 'primary category' on the article content type (utilized for blogs).
- **'bl_url_path':** Saves a standardized version of the original URL on the page, aiding in the URL update process.
- **'bl_clean_date':** Attempts to convert string dates to timestamps, accommodating the inconsistent date formats in the data.
- **'bl_meta_tags':** Constructs the required meta tags for each page.

The blog migration depends on the other two migrations to ensure it runs last, as the post-migration event subscriber is set to process the URLs on the blog migration.




## Additional Fields

Before proceeding with the migration, certain additional fields were added to accommodate specific requirements:

- **field_source_url:** This field was added to the Article, Case Studies, Flexible Pages, and People content types to store the original URL of each page. This allows for the updating of content links during the migration process.

- **field_secondary_categories:** This field was added to the Case Studies and Flexible Pages content types. While it already existed on the Article content type due to its use in the designs, it was added to the other two page types for completeness. The field is primarily used to store category data, although it is otherwise unused.



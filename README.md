# django drive

This is our python project made in Django.

## Installation

To run this drive, you first need to install some python dependencies.
You will need to create a python environment using venv or conda or anything else.

For example using venv :

```
python -m venv .venv
```

Then to activate it :

```
source .venv/bin/activate
```

Next, you need to install the dependencies in the 'requirements.txt' :

```
pip install -r requirements.txt
```

## Configuration

You will find a `db.sqlite3` in the directory. If there is a connection issue or you want simply to start from a blank database, simply delete this sqlite3 file, and run :

To build the migrations :

For the drive application, run

```
python manage.py makemigrations drive
```

And for the authentication application, run :

```
python manage.py makemigrations authentication
```

Then, to apply these migrations :

```
python manage.py migrate
```

## Running

To start the drive, you will have to run the following command :

```
python manage.py runserver
```

## Usage

In this application, you will find the following features :

| Feature               | Description                                                                                                                                                                                                                                                                                                                           | Statut |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| Folder navigation     | You will see that you can navigate from folder to folder just by clicking on the desired folder. You can then go back to your root folder with the home icon on the top left. A breadcrumb should be visible to go back on your path wherever you want                                                                                | ✅     |
| Folder creation       | You can create a folder by clicking on "new>create a folder". You have just to name it and then validate it                                                                                                                                                                                                                           | ✅     |
| File upload           | You can upload file by clicking on "new>upload a file". No file larger than 40Mo will be accepted, and a user have only 100Mo. If uploading the desired file results to passing through this 100Mo, then the upload will be denied.                                                                                                   | ✅     |
| Delete file or forder | A "delete" button is located under the files and folders. Clicking on it results in the file deletion (on the drive and on the DB)                                                                                                                                                                                                    | ✅     |
| Metadata              | You will see that metadatas are displayed for files and folders                                                                                                                                                                                                                                                                       | ✅     |
| File preview          | You can see that on most types of files, a preview is available for you to see (all types of images, pdf ...)                                                                                                                                                                                                                         | ✅     |
| Authentication        | You can create accounts, each users have their own profiles and can't access other users drives                                                                                                                                                                                                                                       | ✅     |
| Redirection           | If not authenticated, you will be redirected to the login page                                                                                                                                                                                                                                                                        | ✅     |
| File view             | By clicking on files, you can view them exclusively (you can also play videos, view pdfs ...). Attention for pdf : Embedded pdfs viewer may not work, a popup request can be displayed for you to allow. The pdf will then load in an external window. If a file can't be read, a download link will be issued for you to download it | ✅     |

### Manual uploading of files (or folders!)

You can also manually put files or folders (with or without elements inside) in your `storage/<username>`. When navigating to them on the web app, the drive will update its database to add all changements. (you might need to refresh 2 times the page)

## Screenshares

You will find on this [google drive](https://drive.google.com/drive/folders/1Xr8TNg6YbtU5abF8pogqT57gnlRKrhhG?usp=sharing) overviews of features of this project.

If you have any question, feal free to contact us.

Hippolyte DEPARIS
Inès PINGAULT
Anaëlle MAZOUNI
Élina ROSEMBERG

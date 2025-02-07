from fabric.api import env, put, run, local
from os.path import exists

# Define the list of web servers
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your actual server IPs
env.user = 'ubuntu'  # Replace with your SSH username
env.key_filename = 'my_ssh_private_key'  # Replace with your SSH private key path

def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the server
        archive_filename = archive_path.split('/')[-1]  # Get the filename (e.g., web_static_20231010.tgz)
        archive_no_ext = archive_filename.split('.')[0]  # Remove the extension (e.g., web_static_20231010)

        # Upload the archive to /tmp/
        put(archive_path, "/tmp/{}".format(archive_filename))

        # Create the target directory
        run("mkdir -p /data/web_static/releases/{}/".format(archive_no_ext))

        # Uncompress the archive to the target directory
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_filename, archive_no_ext))

        # Remove the uploaded archive from /tmp/
        run("rm /tmp/{}".format(archive_filename))

        # Move contents to the proper location
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(archive_no_ext, archive_no_ext))

        # Remove the now-empty web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_no_ext))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(archive_no_ext))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False

from __future__ import print_function
import os
import sys

images = ["ubuntu14", "ubuntu16", "ubuntu18", "debian8", "debian9","centos6", "oracle6", "oracle7"]
omsbundle="<oms-bundle-file>"
workspaceId="<workspace-id"
workspaceKey="<workspace-key>"

def replace_items(infile,old_word,new_word):
    if not os.path.isfile(infile):
        print ("Error on replace_word, not a regular file: "+infile)
        sys.exit(1)

    f1=open(infile,'r').read()
    f2=open(infile,'w')
    m=f1.replace(old_word,new_word)
    f2.write(m)


replace_items("omsfiles/perf.conf", "<workspace-id>", workspaceId)

for image in images:
    container = image + "-container"
    os.system("docker container stop {}".format(container))
    os.system("docker container rm {}".format(container))
    os.system("docker run --name {} -it --privileged=true -d {}".format(container, image))
    os.system("docker cp omsfiles/ {}:/home/temp/".format(container))
    os.system("docker exec {} dos2unix /home/temp/omsfiles/omsSetup.sh".format(container))
    os.system("docker exec {} sh /home/temp/omsfiles/{} --purge".format(container, omsbundle))
    os.system("docker exec {} sh /home/temp/omsfiles/{} --upgrade -w {} -s {}".format(container, omsbundle, workspaceId, workspaceKey))
    os.system("docker exec {} sh /home/temp/omsfiles/omsSetup.sh".format(container))
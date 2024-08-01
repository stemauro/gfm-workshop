# Create your user on our clusters

These guidelines refer to the following notes: https://zhukov1.pages.jsc.fz-juelich.de/intro2sc-handson/docs/access.

Instructions to accomplish the following steps are explained in detail within different sections/subsections of the above notes. Please, refer to the section/subsection whose title is `<TITLE>` whenever you get to any of the following bullet point stating "*follow section/subsection `<TITLE>`*".

- Join a compute time project on JuDoor:
    - use link: [https://judoor.fz-juelich.de/projects/join/training2420](https://judoor.fz-juelich.de/projects/join/training2420)
    - you will have to sign the Usage Agreement for each resource ([video](https://drive.google.com/file/d/1mEN1GmWyGFp75uMIi4d6Tpek2NC_X8eY/view))

- Access the system by:
    - generating a key pair with *OpenSSH*:
        - follow subsection [Generating a key pair with OpenSSH](https://zhukov1.pages.jsc.fz-juelich.de/intro2sc-handson/docs/access/#generating-a-key-pair-with-openssh)
    - uploading the key to JuDoor
        - you will need to find your IP(v4) address (try [here](https://www.whatismyip.com/)) and tweak it, namely
        - if your IP address is `93.199.55.163`, then turn it into `93.199.0.0/16,10.0.0.0/8`
        - follow subsection [Uploading the public key](https://zhukov1.pages.jsc.fz-juelich.de/intro2sc-handson/docs/access/#uploading-the-public-key) using your tweaked IP address
        - repeat the process for every resource listed under "Budget `training2420`"

- Log in to the system via [Jupyter-JSC](https://jupyter.jsc.fz-juelich.de/hub/login):
     - if this is your first time using Jupyter-JSC you will have to register your JuDoor account
     - you will receive a request for account confirmation to the email address associated with your JuDoor account
     - follow subsection [JupyterLab](https://zhukov1.pages.jsc.fz-juelich.de/intro2sc-handson/docs/access/#jupyterlab)
     - ~~create a new notebook using the following configutation values ![](https://gist.github.com/assets/80677000/3e65282f-8152-48d8-badd-d7aef14d0d3b)~~

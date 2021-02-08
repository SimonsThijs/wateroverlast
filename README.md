# Wateroverlast repo

Setup:
```
git clone https://github.com/SimonsThijs/wateroverlast.git
cd wateroverlast

# between these steps I set up my virtualenv but this is not necessary

export PYTHONPATH=$PYTHONPATH:$(pwd)
pip install -r requirements.txt
```

You can download the .TIF files using the supplied script: hoogtekaart/download_ahn3.py. Or you can download the .TIF files from a repo and place them into the folder hoogtekaart/AHN3_data.
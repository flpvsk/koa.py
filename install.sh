hg clone https://code.google.com/p/tulip/ tulip
cd tulip
python setup.py install
cd ..
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
pip install -r requirements.txt

git config --global user.name hkato
git config --global user.email hiroharu.kato.1989.10.13@gmail.com

cd scripts
python build.py
cd ../
find ./ -name "*~" -exec rm {} \;
git add *
git commit -a
git push

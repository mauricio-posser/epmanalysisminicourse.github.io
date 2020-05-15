https://github.com/damianavila/RISE

conda install -c conda-forge rise
ou
pip install RISE


GitHub
https://github.com/damianavila/RISE.git


Para gerar versão Estática:

1. No dir. do slides01_PythonIntro.ipynb rodar o seguinte comando para gerar a vesão estática em html:
jupyter-nbconvert --to slides .\slides02_EPMWebApiIntro.ipynb --reveal-prefix=reveal.js
jupyter-nbconvert --to slides .\slides03_EPMWebApiBonus.ipynb --reveal-prefix=reveal.js

2. Mover a versão gerada (slides01_PythonIntro.slides.html) para o dir Jupyter Sildes onde está o reveal

Esta versão é FLAT!!!

Se desejar gerar a apresentação e subir ela pronta em um servidor local:
1. Executar no Jupyter o arquivo slides01_PythonIntro.ipynb para que todos os resultados estejam presentes;
2. Rodar o comando para subir um servidor local para apresentação de slides gerado automaticamente pelo comando:
jupyter-nbconvert --to slides slides02_EPMWebApiIntro.ipynb --post serve
jupyter-nbconvert --to slides slides03_EPMWebApiBonus.ipynb --post serve
3. O arquivo HTML assim gerado, já abre no formato de apresentação de slides, e pode ser tbm utilziado.

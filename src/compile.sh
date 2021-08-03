python -m compileall ./
chmod +x ./build_utils.pyc
chmod +x ./main.pyc
chmod +x ./parse_opts.pyc

mv ./build_utils.pyc ../bin/
mv ./main.pyc build_exec
mv ./parse_opts.pyc parse_opts
mv ./build_exec ../bin/
mv ./parse_opts ../bin/
rm -rf setup_pq.pyc
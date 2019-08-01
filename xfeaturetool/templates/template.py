{% extends 'base.py' %}

{% block pipefunc %}
    def pipefunc(self, params_tuple):
        seq_no, vals = params_tuple
        # Skip the first empty sequence
        if vals == []:
            return seq_no, None
        sep = '\t'
        vals = np.array([np.array(v.decode().strip("\n").split(sep)) for v in vals], order='F') 

        # If use time index vadility
        result = [v for v in np.take(vals, self.key_index, axis=1)[0]]

        # Loop over defined filters
        filter_lst = [None]
        {% for FILTER in FILTERS -%}

        filter_idx = [ self.col_index[f] for f in {{ FILTER.feature }} ]
        slim_filter_arr = np.take(vals, filter_idx, axis=1)
        filter_cond = {{ FILTER.func }}(condition={{ FILTER.condition }}, arr=slim_filter_arr)
        filter_lst.append(filter_cond)

        {% endfor %}

        # Loop over defined time window
        for tw, filter_cond in product({{ TIME_WINDOW }}, filter_lst):
            tm_cond = np.array([True] * vals.shape[0])
            combine_cond = tm_cond & filter_cond if filter_cond else tm_cond

            vals = np.compress(combine_cond, vals, axis=0)
            
            {% for FEATURE_ENTRY in FEATURE_ENTRIES -%} 

            f_idx = [ self.col_index[f] for f in {{ FEATURE_ENTRY.feature }} ]
            f_arr = np.take(vals, f_idx, axis=1)
            if '{{ FEATURE_ENTRY.preprocess }}' != '':
                f_arr = np.array([{{ FEATURE_ENTRY.preprocess }}(v) for v in f_arr])
            _rslt = [ {{ FEATURE_ENTRY.func }}(v) for v in f_arr]
            for d in _rslt:
                result.append(d)

            {% endfor %}

        return seq_no, result
{% endblock %}

{% block main %}
raw = {{ RAW_PATH }}
result_file_path = {{ RESULT_PATH }}
sep = '\t'
conf = {
    "index" : [{{ PRIMARYKEY }}],
}

domain = {{ DOMAIN }}
cn_domain = {{ CN_DOMAIN }}

config = Conf(path=raw, conf=conf, sep=sep, domain=domain, cn_domain=cn_domain) 
pool = Pool(1)
with open(raw, "rb") as input_file, open(result_file_path, "w") as output_file:
    output_file.write(sep.join(config.output_header) + '\n')
    output_file.write(sep.join(config.output_cn_header) + '\n')
    input_file.readline()
    for seq_no, out_data in pool.imap(config.pipefunc, \
        __enumerate_group(input_file, config.apply_key), chunksize=10):
        if seq_no == 0:
            continue
        output_file.write(sep.join([str(v) for v in out_data]) + "\n")
{% endblock %}
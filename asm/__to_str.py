# CPP functions for converting object to string

num_to_str = 'template <class T>\nstring num_to_str(T number){\n    return to_string(number);\n}'

num_arr_to_str = 'template <class T>\nstring num_arr_to_str(vector<T> arr)\n{\nstring output = "[";\nfor (int i = 0; i < arr.size(); i++) output += to_string(arr[i]) + ",";\noutput += "]";\nreturn output;\n}'



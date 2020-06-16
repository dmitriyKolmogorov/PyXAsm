# Each function in this module is CPP function, that converts string to different objects.

str_to_num = '''template <class T>
T str_to_num(string str)
{
  int is_float = 0;
  for (int i = 0; i < str.size(); i++) if (str[i] == '.') is_float = 1;

  if (is_float == 1) return atof(str.c_str());
  else return atoll(str.c_str());
}'''


str_to_num_arr = '''template <class T>
T * string_to_number_arr(string str, int &n)
{
  int count = 0, is_float = 0;
  for(int i = 0; i < str.size(); i++)
  {
    if (str[i] == ',') count++;
    if (str[i] == '.') is_float = 1;
  }
  n = count + 1;

  T * p = (T *) malloc(n * sizeof(T));

  int index = 0;
  string buffer = "";

  for(int i = 1; i < str.size() - 1; i++)
  {
    if (str[i] == ',')
    {
      if (is_float == 1) p[index] = atof(buffer.c_str());
      else p[index] = atoll(buffer.c_str());
      buffer = "";
      index++;
    } 
    else if (str[i] != ' ') buffer += str[i];
  }

  if (buffer != "")
  {
    if (is_float == 1) p[index] = atof(buffer.c_str());
    else p[index] = atol(buffer.c_str());
  }

  return p;
}'''

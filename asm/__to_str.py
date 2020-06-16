# CPP functions for converting object to string

num_to_str = '''template <class T>
string num_to_str(T number)
{
    return to_string(number);
}'''

num_arr_to_str = '''template <class T>
string num_arr_to_str(T * arr, int n)
{
  string output = "[";
  for (int i = 0; i < n; i++)
  {
    output += to_string(arr[i]);
    output += ',';
  }

  return output + "]";
}'''
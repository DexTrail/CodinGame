/*
 * Palindromic Decomposition
 * https://www.codingame.com/ide/puzzle/palindromic-decomposition
 *
 * Version: 0.3
 * Created: 08/07/2019
 * Last modified: 08/07/2019
 */

using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;

class Solution {
	/// <summary>
	/// Asymmetric string
	/// </summary>
	static int Asymmetric (int x, int v) {
		// res = 3 * x + (v - 3)
		return 3 * x + (v - 3);
	}
	
	/// <summary>
	/// Symmetric string
	/// </summary>
	static int Symmetric (int x) {
		// n = x - 2
		// res = n * (n + 1) / 2
		// Total = Asymmetric + Symmetric
		int n = x - 2;
		return (int)(n * (n + 1) / 2);
	}
	
	/// <summary>
	/// General case (no patterns in the string)
	/// </summary>
	static int General (string str) {
		int result = 0;
		int length = str.Length;

		for (int i = 0; i < length; i++) {
			string str1 = str.Substring (0, i + 1);
			string str1Set = new string (str1.ToCharArray ().Distinct ().ToArray ());
			string str1Rev = new string (str1.Reverse ().ToArray ());
			if (str1.Length == 1 || str1 == str1Rev) {
				if (i == length - 1) {
					result += 3;
					break;
				}

				for (int j = i + 1; j < length; j++) {
					string str2 = str.Substring (i + 1, j - i);
					string str2Set = new string (str2.ToCharArray ().Distinct ().ToArray ());
					string str2Rev = new string (str2.Reverse ().ToArray ());
					if (str2Set.Length == 1 || str2 == str2Rev) {
						if (j == length - 1) {
							result += 3;
							continue;
						}

						string str3 = str.Substring (j + 1);
						string str3Set = new string (str3.ToCharArray ().Distinct ().ToArray ());
						string str3Rev = new string (str3.Reverse ().ToArray ());
						if (str3Set.Length == 1 || str3 == str3Rev)
							result++;
					}
				}
			}
		}
		return result;
	}

	static void Main (string[] args) {
		// Main input
		string inputString = Console.ReadLine ();

		int length = inputString.Length;
		int result = 0;
		string str = "";
		int x = 1;

		string inputStringSet = new string (inputString.ToCharArray ().Distinct ().ToArray ());
		if (inputStringSet.Length == 1) {
			result = Asymmetric (length, 3);
			if (length >= 3)
				result += Symmetric (length);
		} else {
			for (int i = 0; i < (int)(length / 2); i++) {
				str += inputString[i];
				int step = str.Length;
				if (length % step != 0)
					continue;

				for (int j = i + 1; j <= length - step; j += step) {
					if (str != inputString.Substring (j, step)) {
						x = 1;
						break;
					}
					x++;
				}
				if (x != 1)
					break;
			}
			if (x == 1)
				str = inputString;

			result = General (str);
			if (x != 1) {
				int v = result;
				result = Asymmetric (x, v);
				string strRev = new string (str.Reverse ().ToArray ());
				if (str == strRev) {
					result += Symmetric (x);
					if (str.Substring (0, (int)(str.Length / 2) + 1) == str.Substring ((int)(str.Length / 2)))
						result--;
				}
			}
		}

		Console.WriteLine (result.ToString ());
	}
}
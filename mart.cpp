#include <bits/stdc++.h>

using namespace std;

vector <int> pref;

long long int PierwszaWiekszaRowna(long long int poczatek, long long int koniec, long long int szukana){
    long long med;

    if (szukana > pref[koniec])
        return -1;

    while (poczatek < koniec){
        med = (poczatek + koniec) / 2;

        if (pref[med] >= szukana)
            koniec = med;
        else
            poczatek = med + 1;
    }

    if (pref[koniec] > szukana)
        koniec--;

    return koniec;
    
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);


    int z;
    cin >> z;
    for (long long int q = 0; q < z; q++){

        int n, k;
        // n --> liczba ksiazek
        // k --> liczba kuponów
        cin >> n >> k;

        //wagi poszczegolnych ksiazek
        vector <int> wagi;
        pref.clear();
        wagi.resize(n + 1);
        pref.resize(n + 1);

        //wczytanie wag ksiazek --> obliczenie sum prefiksowych
        for (int i = 1; i <= n; i++){
            cin >> wagi[i];
            pref[i] = pref[i - 1] + wagi[i];
//            cout << pref[i] << " ";
        }
//        cout << endl;

        long long int malo = pref[n];
        long long int vk = pref[n], vp = pref[1];


        long long int szukana = (vp + vk) / 2;
        long long int index = PierwszaWiekszaRowna(1, n, szukana);
        long long int kupony = 1;
        long long int szukana_next = pref[index];

//        cout << "szukana:" << szukana << " kupony:" << kupony << " szukana_next:" << szukana_next << " index:" << index << "\n";

        while (vp < vk){
            while (kupony <= k && szukana_next < pref[n] && index > -1){
//                cout << "kupony:" << kupony << " szukana_next:" << szukana_next << " index:" << index << " vp:" << vp << " vk:" << vk << "\n";
                szukana_next = pref[index] + szukana;
                index = PierwszaWiekszaRowna(1, n, szukana_next);
                kupony++;
            }

            if (kupony <= k && (index < 0 || szukana_next >= pref[n])){
                malo = min(malo, szukana);
                vk = szukana - 1;
            } else {
                vp = szukana;
            }

            szukana = (vp + vk + 1) / 2;
//            cout << "kupony:" << kupony << " szukana_next:" << szukana_next << " index:" << index << " MALO:" << malo << " vp:" << vp << " vk:" << vk << "\n";
            index = PierwszaWiekszaRowna(1, n, szukana);
            kupony = 1;
            szukana_next = pref[index];


        }

        cout << malo << "\n";
    }
}

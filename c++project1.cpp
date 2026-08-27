#include<iostream>
#include<fstream>
#include<vector>

using namespace std;

class student 
{
        public :
            int id;
            string name;
            float marks;

                void input()
                {
                    cout << "Enter the ID :- ";
                    cin >> id;
                    cout << "Enter Name :- ";
                    cin.ignore();
                    getline(cin,name);
                    cout << "Enter Marks :- ";
                    cin >> marks; 
                }
                    void display() const
                    {
                        cout << " ID :- " << id << " |  Name :- " << name  << " | Marks :- " << marks << endl;
                    }
};
vector<student>students;
    // load data from file 
        void loadfromfile()
        {
                ifstream file("student . text");
                if(!file) return;
                    student s ;
                        while(file >> s.id)
                        {
                            file.ignore();
                            getline(file,s.name);
                            file >> s.marks;
                            students.push_back(s);
                        }
                        file.close();
        }
        // save data to file
            void savetofile()
            {
                ofstream file("student.txt");
                for(const student &s: students )
                {
                    file << s.id << endl;
                    file << s.name << endl;
                    file << s.marks << endl;
                }
                file.close();
            }
        // add student 
            void addstudent()
            {
                student s;
                    s.input();
                    students.push_back(s);
                    savetofile();
                    cout << "student added successfully! \n";

            }
        // display all  students
            void displayAll()
            {
                if(students.empty())
                {
                    cout << "NO Records Found! \n";
                    return;
                }
                for(const student &s : students)
                {
                    s.display();
                }
            }
        // search student by id 
        void searchstudent()
        {
            int id;
                cout << "Enter Id to search :- ";
                cin >> id;
                    for(const student &s:students)
                    {
                        if(s.id==id)
                        {
                            s.display();
                            return ;
                        }
                    }
                cout << "Student Not Found ! \n";
        }
            // update student 
                void updataStudent()
                {
                    int id ;
                        cout << "Enter id to updata :- ";
                        cin >> id;
                            for(student &s : students)
                            {
                                if(s.id==id)
                                {
                                    cout << "Enter New Details :- \n";
                                    s.input();
                                    savetofile();
                                    cout << "Record Updated ! \n";
                                    return ;
                                }
                            }
                            cout << "student Not found !\n";
                }

            // delete student 
            void deleteStudent()
            { 
                int id;
                    cout << " Enter Id to delete :- ";
                    cin >> id;
                        for(int i=0;i< students.size();i++)
                        {
                            if(students[i].id==id)
                            {
                                students.erase(students.begin()+i);
                                savetofile();
                                cout << "Record Deleted! \n";
                                return;
                            }
                        }
                        cout << "Student Not found! \n";
            }
                int main()
                {
                    loadfromfile();
                        int choice;
                            do{
                                cout << "\n====== student Management System======\n";
                                cout << "1. Add student \n";
                                cout << "2. Dispaly All \n";
                                cout << "3. search student \n";
                                cout << "4. update student \n";
                                cout << "5. Delete student \n";
                                cout << "6. Exit \n";
                                cout << " Enter choice : ";
                                cin >> choice;
                                    switch (choice)
                                    {
                                    case 1: addstudent();
                                        break;
                                    case 2: displayAll();
                                        break;
                                    case 3: searchstudent();
                                        break;
                                    case 4: updataStudent();
                                        break;
                                    case 5:deleteStudent();
                                        break;
                                    case 6: 
                                        cout << "Exiting ......\n";
                                        break;
                
                                    default:
                                    cout << "INVALID Choice ! \n ";
                                    }
                            }while(choice !=6);
                            return 0;
                }
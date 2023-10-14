import { Component, OnDestroy, OnInit, TemplateRef, ViewChild } from "@angular/core";
import { StudentsApiClient } from "../students-api-client.service";
import Student from "../student";
import { Observable, Subject, takeUntil } from "rxjs";

@Component({
  selector: 'app-students-list',
  templateUrl: './students-list.component.html',
  styleUrls: ['./students-list.component.css']
})
export class StudentsListComponent implements OnInit, OnDestroy {

  @ViewChild('readOnlyTemplate', {static: false}) readOnlyTemplate: TemplateRef<any>|null = null;
  @ViewChild('editTemplate', {static: false}) editTemplate: TemplateRef<any>|null = null;

  editedStudent: Student | undefined;
  isNewRecord: boolean = false;
  statusMessage: string = "";
  students: Student[] | undefined;

  private students$ = new Subject<Student[]>();
  private destroy$ = new Subject<void>();

  constructor(private studentsApiClient: StudentsApiClient) { }

  set searchText(searchText: string) {
    this.loadStudents(searchText);
  }

  ngOnInit(): void {
    this.students$
      .pipe(takeUntil(this.destroy$))
      .subscribe(students => this.students = students);
    this.loadStudents();
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadTemplate(student: Student) {
    if (this.editedStudent && this.editedStudent.id == student.id) {
      return this.editTemplate;
    }

    return this.readOnlyTemplate;
  }

  private loadStudents(searchText: string = "") {
    let studentsObservable: Observable<Student[]> = searchText
      ? this.studentsApiClient.find(searchText)
      : this.studentsApiClient.getAll();

    studentsObservable
      .pipe(takeUntil(this.destroy$))
      .subscribe(students => this.students$.next(students));
  }

  addStudent() {
    this.editedStudent = {
      id:"",
      name: "",
      age:24,
    };
    this.students?.push(this.editedStudent);
    this.isNewRecord = true;
  }

  editStudent(student: any) {
    this.editedStudent = {
      id: student.id,
      name: student.name,
      age: student.age,
    }
  }

  deleteStudent(student: any) {
    this.studentsApiClient
      .delete(student.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe(() =>{
          this.statusMessage = 'Данные успешно удалены';
          this.loadStudents();
      });
  }

  cancel() {
    this.loadStudents();
  }

  saveStudent() {
    const studentUpdated$: Observable<any> = this.isNewRecord
      ? this.studentsApiClient.create(this.editedStudent!)
      : this.studentsApiClient.update(this.editedStudent?.id!, this.editedStudent!);

    studentUpdated$
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.statusMessage = 'Данные успешно обновлены';
        this.editedStudent = undefined;
        this.loadStudents();
      });

    this.isNewRecord = false;
  }
}

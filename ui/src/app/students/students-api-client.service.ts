import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import Student from "./student";
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class StudentsApiClient {

  private basePath: string = environment.apiUrl;

  constructor(private httpClient: HttpClient) { }

  create(student: Partial<Student>): Observable<Object> {
    return this.httpClient.post<Student>(this.basePath, student);
  }

  getAll() : Observable<Student[]>{
    return this.httpClient.get<Student[]>(`${this.basePath}`);
  }

  find(searchFilter: string) : Observable<Student[]>{
    return this.httpClient.get<Student[]>(`${this.basePath}/filter?name=${searchFilter}`);
  }

  update(studentId: string, student: Partial<Student>): Observable<Student> {
    return this.httpClient.put<Student>(`${this.basePath}/${studentId}`, student);
  }

  delete(studentId: string): Observable<Object> {
    return this.httpClient.delete(`${this.basePath}/${studentId}`);
  }
}

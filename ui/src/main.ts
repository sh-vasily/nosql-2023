import {enableProdMode, importProvidersFrom} from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { environment } from './environments/environment';
import {StudentsListComponent} from "./app/students/students-list/students-list.component";
import {bootstrapApplication} from "@angular/platform-browser";
import {HttpClientModule} from "@angular/common/http";

if (environment.production) {
  enableProdMode();
}

bootstrapApplication(StudentsListComponent, {
  providers: [importProvidersFrom(HttpClientModule)]
  })
  .catch(err => console.error(err));

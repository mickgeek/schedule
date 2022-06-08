import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { APP_CONFIG, ENVIRONMENT } from './app.config';
import { RoutingModule } from './routing.module';
import { AppComponent } from './app.component';
import { IndexComponent } from './index/index.component';
import { AuthenticationComponent } from './authentication/authentication.component';
import { UserComponent } from './user/user.component';
import { TaskComponent } from './task/task.component';
import { ErrorNotFoundComponent } from './error-not-found/error-not-found.component';
import { UserTokenService } from './user-token.service';
import { RequestService } from './request.service';

@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatToolbarModule,
    MatTableModule,
    MatInputModule,
    MatRadioModule,
    MatButtonModule,
    MatDividerModule,
    MatIconModule,
    RoutingModule
  ],
  declarations: [
    AppComponent,
    IndexComponent,
    AuthenticationComponent,
    UserComponent,
    TaskComponent,
    ErrorNotFoundComponent
  ],
  providers: [
    { provide: APP_CONFIG, useValue: ENVIRONMENT },
    UserTokenService,
    RequestService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

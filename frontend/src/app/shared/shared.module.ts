import { NgModule } from '@angular/core'
import { CommonModule } from '@angular/common'
import { BrowserModule } from '@angular/platform-browser'
import { HttpClientModule } from '@angular/common/http'
import { FormsModule, ReactiveFormsModule } from '@angular/forms'
import { RouterModule } from '@angular/router'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ManageNavbarComponent } from '@/layout/manage-navbar/manage-navbar.component'
import { NotFoundComponent } from '@/shared/components/not-found/not-found.component'
import { InDevelopmentComponent } from '@/shared/components/in-development/in-development.component'
import { PhoneValidatorDirective } from '@/shared/validators/phone.validator.directive'
import { PasswordValidatorDirective } from '@/shared/validators/password-validator.directive'
import { LoadingComponent } from '@/shared/components/loading/loading.component'
import { DialogConfirmComponent } from '@/shared/components/dialog-confirm/dialog-confirm.component'


const SHARED = [
    CommonModule,
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    RouterModule,
    FormsModule,
    ReactiveFormsModule
]

const COMPONENTS = [
    ManageNavbarComponent,
    InDevelopmentComponent,
    NotFoundComponent,
    LoadingComponent,
    DialogConfirmComponent,
    PhoneValidatorDirective,
    PasswordValidatorDirective
]


@NgModule( {
    declarations: COMPONENTS,
    imports: SHARED,
    exports: [ ...SHARED, ...COMPONENTS ]
} )
export class SharedModule {}
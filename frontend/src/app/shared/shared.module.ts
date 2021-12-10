import { NgModule } from '@angular/core'
import { CommonModule } from '@angular/common'
import { BrowserModule } from '@angular/platform-browser'
import { HttpClientModule } from '@angular/common/http'
import { FormsModule, ReactiveFormsModule } from '@angular/forms'
import { RouterModule } from '@angular/router'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ManageNavbarComponent } from '@/layout/manage-navbar/manage-navbar.component'
import { NotFoundComponent } from '@/shared/not-found/not-found.component'
import { InDevelopmentComponent } from '@/shared/in-development/in-development.component'


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
    NotFoundComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: SHARED,
    exports: [ ...SHARED, ...COMPONENTS ]
} )
export class SharedModule {}
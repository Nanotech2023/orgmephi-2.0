import { NgModule } from '@angular/core'
import { CommonModule } from '@angular/common'
import { BrowserModule } from '@angular/platform-browser'
import { HttpClientModule } from '@angular/common/http'
import { FormsModule } from '@angular/forms'
import { RouterModule } from '@angular/router'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ManageNavbarComponent } from '@/layout/manage-navbar/manage-navbar.component'


const SHARED = [
    CommonModule,
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    RouterModule,
    FormsModule
]

const COMPONENTS = [
    ManageNavbarComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: SHARED,
    exports: [ ...SHARED, ...COMPONENTS ]
} )
export class SharedModule {}
import { NgModule } from '@angular/core'
import { CommonModule } from '@angular/common'
import { BrowserModule } from '@angular/platform-browser'
import { HttpClientModule } from '@angular/common/http'
import { FormsModule } from '@angular/forms'
import { RouterModule } from '@angular/router'


const SHARED = [
    CommonModule,
    BrowserModule,
    HttpClientModule,
    RouterModule,
    FormsModule
]


@NgModule( {
    imports: SHARED,
    exports: SHARED
} )

export class SharedModule {}
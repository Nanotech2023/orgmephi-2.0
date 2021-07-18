import { NgModule } from '@angular/core'
import { CommonModule } from '@angular/common'
import { BrowserModule } from '@angular/platform-browser'
import { HttpClientModule } from '@angular/common/http'
import { FormsModule } from '@angular/forms'


const SHARED = [
    CommonModule,
    BrowserModule,
    HttpClientModule,
    FormsModule
]


@NgModule( {
    imports: SHARED,
    exports: SHARED
} )

export class SharedModule {}

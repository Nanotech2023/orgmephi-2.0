import { NgModule } from '@angular/core'
import { BrowserModule } from '@angular/platform-browser'
import { AppRoutingModule } from '@/app-routing.module'
import { AppComponent } from '@/app.component'
import { LayoutModule } from '@/layout/layout.module'
import { AboutModule } from '@/about/about.module'
import { FeedbacksModule } from '@/feedbacks/feedbacks.module'
import { OlympiadsModule } from '@/olympiads/olympiads.module'


@NgModule( {
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserModule,
        LayoutModule,
        AboutModule,
        FeedbacksModule,
        OlympiadsModule,
        AppRoutingModule
    ],
    providers: [],
    bootstrap: [ AppComponent ]
} )
export class AppModule
{
}
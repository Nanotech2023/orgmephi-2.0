import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { NotFoundComponent } from '@/shared/not-found/not-found.component'
import { InDevelopmentComponent } from '@/shared/in-development/in-development.component'


const routes: Routes =
    [
        {
            path: '', redirectTo: 'home', pathMatch: 'full'
        },
        {
            path: 'in-development', component: InDevelopmentComponent
        },
        {
            path: '404', component: NotFoundComponent
        },
        {
            path: '**', redirectTo: '404', pathMatch: 'full'
        }
    ]


@NgModule( {
    imports: [ RouterModule.forRoot( routes, { initialNavigation: 'disabled' } ) ],
    exports: [ RouterModule ]
} )
export class AppRoutingModule {}
import { NgModule } from '@angular/core'
import { InitialNavigation, RouterModule, Routes } from '@angular/router'
import { NotFoundComponent } from '@/not-found.component'


const routes: Routes =
    [
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
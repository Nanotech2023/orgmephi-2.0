import { NgModule } from '@angular/core'
import { InitialNavigation, RouterModule, Routes } from '@angular/router'


const routes: Routes =
    [
        {
            path: '**', redirectTo: '/home',
            pathMatch: 'full'
        }
    ]


@NgModule( {
    imports: [ RouterModule.forRoot( routes, { initialNavigation: 'disabled' } ) ],
    exports: [ RouterModule ]
} )
export class AppRoutingModule {}
import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { NotFoundComponent } from '@/shared/not-found/not-found.component'


const routes: Routes =
    [
        {
            path: '', redirectTo: 'home', pathMatch: 'full'
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
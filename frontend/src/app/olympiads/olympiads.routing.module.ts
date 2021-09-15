import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { OlympiadListComponent } from '@/olympiads/containers/olympiad-list/olympiad-list.component'


const routes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'user', component: OlympiadListComponent, canActivate: [ AuthGuardService ]
            }
        ]
    }
]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class OlympiadsRoutingModule {}
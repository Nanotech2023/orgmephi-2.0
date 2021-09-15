import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { ContestListComponent } from '@/contests/containers/contest-list/contest-list.component'
import { ContestDetailsComponent } from '@/contests/containers/contest-details/contest-details.component'


const routes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'contests', component: ContestListComponent, canActivate: [ AuthGuardService ]
            },
            {
                path: 'contests/:id', component: ContestDetailsComponent, canActivate: [ AuthGuardService ]
            }
        ]
    }
]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ContestsRoutingModule {}
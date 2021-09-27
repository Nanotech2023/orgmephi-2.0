import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { ContestListComponent } from '@/contests/containers/contest-list/contest-list.component'
import { ContestDetailsComponent } from '@/contests/containers/contest-details/contest-details.component'
import { ContestRegistrationComponent } from '@/contests/containers/contest-registration/contest-registration.component'
import { HomeComponent } from '@/contests/containers/home/home.component'
import { ContestListItemComponent } from '@/contests/components/contest-list-item/contest-list-item.component'
import { ContestAssignmentComponent } from '@/contests/containers/contest-assignment/contest-assignment.component'
import { ContestAssignmentItemComponent } from '@/contests/components/contest-assignment-item/contest-assignment-item.component'


export const COMPONENTS = [
    ContestListComponent,
    ContestDetailsComponent,
    ContestListItemComponent,
    ContestRegistrationComponent,
    ContestAssignmentComponent,
    HomeComponent,
    ContestAssignmentItemComponent
]


const routes: Routes =
    [
        {
            path: 'home', component: HomeComponent, canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests', component: ContestListComponent, canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests/:id', component: ContestDetailsComponent, canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests/:id/registration',
            component: ContestRegistrationComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests/:id/assignment', component: ContestAssignmentComponent, canActivate: [ AuthGuardService ]
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ContestsRoutingModule {}
import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { ContestListComponent } from '@/contests/containers/contest-list/contest-list.component'
import { ContestDetailsComponent } from '@/contests/containers/contest-details/contest-details.component'
import { ContestRegistrationComponent } from '@/contests/containers/contest-registration/contest-registration.component'
import { HomeComponent } from '@/contests/containers/home/home.component'
import { ContestListItemComponent } from '@/contests/components/contest-list-item/contest-list-item.component'
import { ContestAssignmentComponent } from '@/contests/containers/contest-assignment/contest-assignment.component'
import {
    ContestAssignmentItemComponent
} from '@/contests/components/contest-assignment-item/contest-assignment-item.component'
import { ContestResultsComponent } from '@/contests/containers/contest-results/contest-results.component'
import { VideoContainerComponent } from '@/contests/containers/video-container/video-container.component'
import {
    ContestAssignmentResultsComponent
} from '@/contests/containers/contest-assignment-results/contest-assignment-results.component'


export const CONTESTS_COMPONENTS = [
    ContestListComponent,
    ContestDetailsComponent,
    ContestListItemComponent,
    ContestRegistrationComponent,
    ContestAssignmentComponent,
    ContestAssignmentResultsComponent,
    HomeComponent,
    ContestAssignmentItemComponent,
    ContestResultsComponent,
    VideoContainerComponent
]


export const CONTEST_ROUTES: Routes =
    [
        {
            path: 'home',
            component: HomeComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests',
            component: ContestListComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests/results',
            redirectTo: 'in-development'
            // component: ContestResultsComponent,
            // canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests/:contestId',
            component: ContestDetailsComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests/:contestId/registration',
            component: ContestRegistrationComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests/:contestId/assignment',
            component: ContestAssignmentComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'contests/:contestId/assignment-results',
            component: ContestAssignmentResultsComponent,
            canActivate: [ AuthGuardService ]
        },

    ]
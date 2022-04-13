import { Routes } from '@angular/router'
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
import {
    ContestAssignmentResultsItemComponent
} from '@/contests/components/contest-assignment-results-item/contest-assignment-results-item.component'
import { ContestDetailsStage3FailureComponent } from '@/contests/components/contest-details-stage3-failure/contest-details-stage3-failure.component'
import { ContestDetailsStage3SuccessComponent } from '@/contests/components/contest-details-stage3-success/contest-details-stage3-success.component'
import { ContestDetailsUnavailableComponent } from '@/contests/components/contest-details-unavailable/contest-details-unavailable.component'
import { ContestDetailsRegisterComponent } from '@/contests/components/contest-details-register/contest-details-register.component'
import {
    ContestDetailsStage5Component
} from '@/contests/components/contest-details-stage5/contest-details-stage5.component'


export const CONTESTS_COMPONENTS = [
    ContestAssignmentResultsItemComponent,
    ContestListComponent,
    ContestDetailsComponent,
    ContestListItemComponent,
    ContestRegistrationComponent,
    ContestAssignmentComponent,
    ContestAssignmentResultsComponent,
    HomeComponent,
    ContestAssignmentItemComponent,
    ContestResultsComponent,
    VideoContainerComponent,
    ContestDetailsStage3FailureComponent,
    ContestDetailsStage3SuccessComponent,
    ContestDetailsUnavailableComponent,
    ContestDetailsRegisterComponent,
    ContestDetailsStage5Component
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
            component: ContestResultsComponent,
            canActivate: [ AuthGuardService ]
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
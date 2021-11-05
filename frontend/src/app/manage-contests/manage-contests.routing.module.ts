import { RouterModule, Routes } from '@angular/router'
import { NgModule } from '@angular/core'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { ManageBaseContestsComponent } from '@/manage-contests/containers/manage-base-contests/manage-base-contests.component'
import { ManageCompositeContestsComponent } from '@/manage-contests/containers/manage-composite-contests/manage-composite-contests.component'
import { ManageCompositeContestStagesComponent } from '@/manage-contests/containers/manage-composite-contest-stages/manage-composite-contest-stages.component'
import { ManageContestComponent } from '@/manage-contests/containers/manage-contest/manage-contest.component'
import { ManageContestVariantsComponent } from '@/manage-contests/containers/manage-contest-variants/manage-contest-variants.component'
import { ManageContestVariantTasksComponent } from '@/manage-contests/containers/manage-contest-variant-tasks/manage-contest-variant-tasks.component'
import { ManageContestUsersComponent } from '@/manage-contests/containers/manage-contest-users-component/manage-contest-users.component'
import { ManageContestUserAssignmentComponent } from '@/manage-contests/containers/manage-contest-user-assignment/manage-contest-user-assignment.component'


export const COMPONENTS = [
    ManageBaseContestsComponent,
    ManageCompositeContestsComponent,
    ManageCompositeContestStagesComponent,
    ManageContestComponent,
    ManageContestUsersComponent,
    ManageContestUserAssignmentComponent,
    ManageContestVariantsComponent,
    ManageContestVariantTasksComponent
]

const routes: Routes =
    [
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages/:stageId/contest/:simpleContestId/variants/:variantId/tasks',
            component: ManageContestVariantTasksComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages/:stageId/contest/:simpleContestId/variants',
            component: ManageContestVariantsComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages/:stageId/contest/:simpleContestId/users/:userId/assignment',
            component: ManageContestUserAssignmentComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages/:stageId/contest/:simpleContestId/users',
            component: ManageContestUsersComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages/:stageId',
            component: ManageContestComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages/:stageId',
            component: ManageContestComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId/composite/:compositeContestId/stages',
            component: ManageCompositeContestStagesComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage/contests/:baseContestId',
            component: ManageCompositeContestsComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage/contests',
            component: ManageBaseContestsComponent,
            canActivate: [ AuthGuardService ]
        },
        {
            path: 'manage', redirectTo: "manage/contests"
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ManageContestsRoutingModule {}
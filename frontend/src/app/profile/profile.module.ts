import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { ProfileRoutingModule } from '@/profile/profile.routing.module'
import { ProfileViewComponent } from '@/profile/containers/profile-view/profile-view.component'
import { ProfileEditDocumentComponent } from '@/profile/components/profile-edit-document/profile-edit-document.component'
import { ProfileEditPersonalComponent } from '@/profile/components/profile-edit-personal/profile-edit-personal.component'
import { ProfileEditLimitationsComponent } from '@/profile/components/profile-edit-limitations/profile-edit-limitations.component'
import { ProfileEditDwellingComponent } from '@/profile/components/profile-edit-dwelling/profile-edit-dwelling.component'
import { ProfileEditSchoolComponent } from '@/profile/components/profile-edit-school/profile-edit-school.component'
import { YesNoComponentComponent } from '@/profile/components/yes-no-component/yes-no-component.component'


const COMPONENTS = [
    ProfileViewComponent,
    ProfileEditPersonalComponent,
    ProfileEditDocumentComponent,
    ProfileEditDwellingComponent,
    ProfileEditLimitationsComponent,
    ProfileEditSchoolComponent,
    YesNoComponentComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        ProfileRoutingModule
    ]
} )
export class ProfileModule {}
